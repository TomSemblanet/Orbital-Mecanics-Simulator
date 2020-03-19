import matplotlib.pyplot as plt
import numpy as np 
import math

import celestial_body as c_b
import constants as cst
import numerical_integration as n_i
import utility_functions as u_f

class Orbit :

	def __init__ (self, satellite, r0, v0, corps_ref) : 

		(self.a, self.e, self.i, self.Lnode, self.Lperi, self.true_anomaly, self.ecc_vect, self.n, self.n_std) = u_f.CartesianToKeplerian(r0, v0, corps_ref.mu, all=True)
		self.corps_ref = corps_ref
		satellite.true_anomaly = self.true_anomaly

		self.R1 = np.array([ [math.cos(self.Lperi), -math.sin(self.Lperi), 0.],
			            	 [math.sin(self.Lperi),  math.cos(self.Lperi), 0],
			             	 [                  0.,                    0., 1.] ])

		self.R2 = np.array([ [1.,               0.,               0.],
			             	[0.,  math.cos(self.i), -math.sin(self.i)],
			             	[0.,  math.sin(self.i),  math.cos(self.i)] ])

		self.R3 = np.array([ [math.cos(self.Lnode), -math.sin(self.Lnode),     0.],
			             	[math.sin(self.Lnode),  math.cos(self.Lnode),     0.],
			             	[                  0.,                    0.,     1.] ])

		self.traj = np.array([ [], [], [] ])

		if(self.e < 1) : 
			self.T = 2*math.pi * math.sqrt( self.a*self.a*self.a/corps_ref.mu )
			
			self.perigee_radius = self.a*(1-self.e)
			self.apogee_radius = self.a*(1+self.e)
			self.perigee_velocity = math.sqrt(corps_ref.mu*(2/self.perigee_radius - 1/self.a))
			self.apogee_velocity = math.sqrt(corps_ref.mu*(2/self.apogee_radius - 1/self.a))		

		else : 
			self.T = 0

			self.perigee_radius = self.a*(1-self.e)
			self.apogee_radius = 0.
			self.perigee_velocity = math.sqrt(corps_ref.mu*(2/self.perigee_radius - 1/self.a))
			self.apogee_velocity = 0.

		self.PathModelCalculation()

	def PathModelCalculation (self) : 

		if(self.e < 1) :
			true_anomaly_array = np.linspace(0, 2*math.pi, 1000) 
		else :
			thetaM = math.acos(-1/self.e)
			true_anomaly_array = np.linspace(-thetaM*0.9999, thetaM*0.9999, 1000)

		h = math.sqrt(self.corps_ref.mu*self.a*(1-self.e**2))

		coordinates = np.array([ [], [], [] ])

		for u in true_anomaly_array : 
			x = (h*h/self.corps_ref.mu)*(1/(1+self.e*math.cos(u))) * math.cos(u)
			y = (h*h/self.corps_ref.mu)*(1/(1+self.e*math.cos(u))) * math.sin(u)
			coordinates = np.append(coordinates, np.array([ [x], [y], [0] ]), axis=1)

		self.traj = self.R3.dot(self.R2.dot(self.R1.dot(coordinates)))
		