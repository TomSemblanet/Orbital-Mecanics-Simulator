import matplotlib.pyplot as plt
import numpy as np
import random 
import math

import parameters as prm
import constants as cst
import utility_functions as u_f
import orbit as orb


class CelestialBody : 

	celestial_bodies = []

	def __init__ (self, name, corps_ref=None) :

		self.name = name
		self.color = cst.Celestial_Bodies_Dict[self.name]["color"]
		self.central = (cst.Celestial_Bodies_Dict[self.name]['central'] == True)

		self.influence_sphere_radius = 0.
		self.mass = cst.Celestial_Bodies_Dict[self.name]["mass"]
		self.mu = cst.Celestial_Bodies_Dict[self.name]["mu"]
		self.radius = cst.Celestial_Bodies_Dict[self.name]["radius"]

		self.corps_ref = corps_ref

		self.r_abs = cst.Celestial_Bodies_Dict[self.name]['initial_position']
		if (self.central) : self.r_abs = np.array([0., 0., 0.])
		self.r_abs_norm = np.linalg.norm(self.r_abs)

		self.r_cr = self.r_abs
		self.r_cr_norm = np.linalg.norm(self.r_cr)
		
		self.v_abs = cst.Celestial_Bodies_Dict[self.name]['initial_velocity']
		if (self.central) : self.v_abs = np.array([0., 0., 0.])
		self.v_abs_norm = np.linalg.norm(self.v_abs)

		self.v_cr = self.v_abs
		self.v_cr_norm = np.linalg.norm(self.v_abs)

		self.h_cr = np.array([0., 0., 0.])
		self.h_cr_norm = 0.

		self.true_anomaly = 0.
		self.initial_true_anomaly = 0.

		self.E = 0.
		self.M = 0.

		self.eps = 0.4090928
		self.a0 = 0
		self.d0 = 0

		self.R1R3 = np.array([[ math.cos(math.pi/2+self.a0)                             ,  math.sin(math.pi/2+self.a0)                             ,                          0.],
			             	  [-math.sin(math.pi/2+self.a0)*math.cos(math.pi/2-self.d0) ,  math.cos(math.pi/2-self.d0)*math.cos(math.pi/2+self.a0) , math.sin(math.pi/2-self.d0)],
			             	  [ math.sin(math.pi/2-self.d0)*math.sin(math.pi/2+self.a0) ,  -math.sin(math.pi/2-self.d0)*math.cos(math.pi/2+self.a0), math.cos(math.pi/2-self.d0)]])
		self.invR1R3 = np.linalg.inv(self.R1R3) 

		self.moving_body = not(np.linalg.norm(self.r_abs) == 0)

		if (self.central == False) : 
			self.loadParameters()

	#################################################
	#
	# DESCRIPTION : calculates all the parameters of the celestial body at construction.
	#				calculates rotations needed to go in the orbital plan from the referent body plan.
	#
	#################################################

	def loadParameters (self) :

		if(self.corps_ref.name != 'Sun') : # to know, in the case of a natural satellite
			self.r_cr, self.v_cr = self.corps_ref.Helio2Planeto(self)

		self.r_cr_norm = np.linalg.norm(self.r_cr)
		self.v_cr_norm = np.linalg.norm(self.v_cr)

		self.h_cr = np.cross(self.r_cr, self.v_cr)
		self.h_cr_norm = np.linalg.norm(self.h_cr)

		self.orbit = orb.Orbit(self.r_cr, self.v_cr, self.corps_ref)
		if(self.corps_ref.name != 'Sun') :
			self.orbit.traj = np.array([ [1.,  0., 0.], [0.,  math.cos(self.corps_ref.eps), -math.sin(self.corps_ref.eps)], [0.,  math.sin(self.corps_ref.eps),  math.cos(self.corps_ref.eps)] ]).dot(self.orbit.traj)

		self.influence_sphere_radius = self.orbit.a * (self.mass/self.corps_ref.mass)**(2/5)
		
		# True anomaly : setted in the orbitals parameters calculation (orbit constructor)
		self.initial_true_anomaly = self.true_anomaly

		self.E = 2*math.atan( math.sqrt((1-self.orbit.e)/(1+self.orbit.e)) *  math.tan(self.true_anomaly/2))
		self.M = self.E - self.orbit.e*math.sin(self.E)


	def __str__ (self) : 

		try : 
			return '> {}\n'.format(self.name) + \
			   '- Semi-major axis (a) : {} km\n'.format(round(self.orbit.a/1000, 0)) + \
			   '- Eccentricity (e) : {}\n'.format(round(self.orbit.e, 5)) + \
			   '- True anomaly : {} °\n'.format(round(self.true_anomaly*180/math.pi, 4)) + \
			   '- Longitude of perigee : {} °\n'.format(round(self.orbit.Lperi*180/math.pi, 2)) + \
			   '- Longitude of ascendant node : {} °\n'.format(round(self.orbit.Lnode*180/math.pi, 2)) + \
			   '- Inclinaison : {} °\n'.format(round(self.orbit.i*180/math.pi, 20)) + \
			   '- Period : {} sec\n'.format(round(self.orbit.T, 2)) + \
			   '- Distance : {} km\n'.format(round(self.r_cr_norm/1000, 2)) + \
			   '- Cartesian Coord : {}\n'.format(self.r_cr) + \
			   '- Cartesian Velocity : {}\n'.format(self.v_cr)

		except : 
			print("=_=_=_=  You try to display the parameters of the central body  =_=_=_=\n")
			exit()

	

	def set_position (self) : 

		"""
		Computes the new position of the celestial body following Kepler's laws and by solving the Kepler's equation (Newton's method)

		"""

		self.M = self.M + (2*math.pi/self.orbit.T)*prm.parameters["time"]["time step"]
		self.E = self.M

		delt = 1

		while(delt > 1e-6) : 
			new_E = self.E - (self.E - self.orbit.e*math.sin(self.E) - self.M)/(1 - self.orbit.e*math.cos(self.E))
			delt = abs(new_E - self.E)
			self.E = new_E

		self.true_anomaly = 2*math.atan( math.sqrt( (1+self.orbit.e)/(1-self.orbit.e) ) * math.tan(self.E/2))

		self.r_cr = self.orbit.R3.dot(self.orbit.R2.dot(self.orbit.R1.dot(np.array([self.orbit.a * (math.cos(self.E)-self.orbit.e), self.orbit.a * math.sqrt(1-self.orbit.e*self.orbit.e)*math.sin(self.E), 0]))))
		self.r_cr_norm = np.linalg.norm(self.r_cr)

		self.v_cr = self.orbit.R3.dot(self.orbit.R2.dot(self.orbit.R1.dot(np.array([- math.sqrt( self.corps_ref.mu/(self.orbit.a*(1-self.orbit.e*self.orbit.e)) )*math.sin(self.true_anomaly), 
																  math.sqrt( self.corps_ref.mu/(self.orbit.a*(1-self.orbit.e*self.orbit.e)) )*(self.orbit.e+math.cos(self.true_anomaly)),
																  0.]))))
		self.v_cr_norm = np.linalg.norm(self.v_cr)

		if(self.corps_ref.name != 'Sun') : 

			self.r_abs, self.v_abs = self.corps_ref.Planeto2Helio(self)

			# self.r_abs = self.r_cr + self.corps_ref.r_cr
			# self.r_abs_norm = np.linalg.norm(self.r_abs)

			# self.v_abs = self.v_cr + self.corps_ref.v_cr
			# self.v_abs_norm = np.linalg.norm(self.v_abs)

		else : 
			self.r_abs = self.r_cr
			self.r_abs_norm = self.r_cr_norm

			self.v_abs = self.v_cr 
			self.v_abs_norm = self.v_cr_norm


	def HelioPlaneto (self, body, h2p=True) : 

		if(h2p == True) : 

			obliquity_matrix = np.array([ [1.,                   0.,                   0.],
			             				  [0.,  math.cos(-self.eps), -math.sin(-self.eps)],
			             				  [0.,  math.sin(-self.eps),  math.cos(-self.eps)] ])

			new_r = obliquity_matrix.dot(self.r_abs - body.r_cr)
			new_v = obliquity_matrix.dot(self.v_abs - body.v_cr)



		else : 
			obliquity_matrix = np.array([ [1.,                  0.,                  0.],
			             				  [0.,  math.cos(self.eps), -math.sin(self.eps)],
			             				  [0.,  math.sin(self.eps),  math.cos(self.eps)] ])

			new_r = self.r_abs + obliquity_matrix.dot(body.r_cr)
			new_v = self.v_abs + obliquity_matrix.dot(body.v_cr)

		return new_r, new_v

	def getObliquityMatrix (self, h2p=True) : 

		if(h2p == True) : 
			return np.array([ [1.,                   0.,                   0.],
			             	  [0.,  math.cos(-self.eps), -math.sin(-self.eps)],
			             	  [0.,  math.sin(-self.eps),  math.cos(-self.eps)]])
		else : 
			return np.array([ [1.,               0.,                       0.],
			             	  [0.,  math.cos(self.eps),   -math.sin(self.eps)],
			             	  [0.,  math.sin(self.eps),    math.cos(self.eps)]])


	def Helio2Planeto (self, body) : 
		
		obliquity_matrix = self.getObliquityMatrix(h2p=True)

		new_r = obliquity_matrix.dot(body.r_cr - self.r_abs)
		new_v = obliquity_matrix.dot(body.v_cr - self.v_abs)

		if(self.name not in ['Earth', 'Moon']) : 
			new_r = self.R1R3.dot(new_r)
			new_v = self.R1R3.dot(new_v)

		return new_r, new_v

	def Planeto2Helio (self, body) : 
		
		obliquity_matrix = self.getObliquityMatrix(h2p=False)

		if(self.name not in ['Earth', 'Moon']) : 
			new_r = self.r_abs + obliquity_matrix.dot(self.invR1R3.dot(body.r_cr))
			new_v = self.v_abs + obliquity_matrix.dot(self.invR1R3.dot(body.v_cr))
		else : 
			new_r = self.r_abs + obliquity_matrix.dot(body.r_cr)
			new_v = self.v_abs + obliquity_matrix.dot(body.v_cr)

		return new_r, new_v

	def Planeto2NatSat (self, body) : 

		new_r = body.r_cr - self.r_cr
		new_v = body.v_cr - self.v_cr

		return new_r, new_v 

	def NatSat2Planeto (self, body) : 

		new_r = body.r_cr + self.r_cr
		new_v = body.v_cr + self.v_cr

		return new_r, new_v

