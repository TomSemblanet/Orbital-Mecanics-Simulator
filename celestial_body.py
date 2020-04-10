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

		try :
			self.eps = cst.Celestial_Bodies_Dict[self.name]['eps']
			self.a0 = cst.Celestial_Bodies_Dict[self.name]['a0']
			self.d0 = cst.Celestial_Bodies_Dict[self.name]['d0']
		except : 
			self.eps = 0
			self.a0 = 0
			self.d0 = 0


		self.R_e = np.array([  [1.                      ,                    0.,                   0.],
			                   [0.                      ,   math.cos(-self.eps),  math.sin(-self.eps)],
			                   [0.                      ,  -math.sin(-self.eps),  math.cos(-self.eps)] ])

		self.R_a0 = np.array([ [ math.cos(math.pi/2 + self.a0),    math.sin(math.pi/2 + self.a0),                            0.],
			                   [-math.sin(math.pi/2 + self.a0),    math.cos(math.pi/2 + self.a0),                            0.],
			                   [0.                            ,                               0.,                             1] ])

		self.R_d0 = np.array([ [1.                ,                             0.,                               0.],
			                   [0.                ,  math.cos(math.pi/2 - self.d0),    math.sin(math.pi/2 - self.d0)],
			                   [0.                , -math.sin(math.pi/2 - self.d0),    math.cos(math.pi/2 - self.d0)] ])

		# Étrange place du signe '-', normalement sur le sinus "en haut à droite" ...

		self.rotation_matrix = self.R_d0.dot(self.R_a0.dot(np.linalg.inv(self.R_e)))
		self.inv_rotation_matrix = np.linalg.inv(self.rotation_matrix)

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

		self.r_cr_norm, self.v_cr_norm  = np.linalg.norm(self.r_cr), np.linalg.norm(self.v_cr)

		self.h_cr = np.cross(self.r_cr, self.v_cr)
		self.h_cr_norm = np.linalg.norm(self.h_cr)

		self.orbit = orb.Orbit(self.r_cr, self.v_cr, self.corps_ref)
		if(self.corps_ref.name != 'Sun') :
			self.orbit.traj = self.corps_ref.inv_rotation_matrix.dot(self.orbit.traj)

		self.influence_sphere_radius = self.orbit.a * (self.mass/self.corps_ref.mass)**(2/5)

		self.true_anomaly = self.orbit.true_anomaly
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
			   '- Inclinaison : {} °\n'.format(round(self.orbit.i*180/math.pi, 5)) + \
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
			self.r_abs_norm, self.v_abs_norm = np.linalg.norm(self.r_abs), np.linalg.norm(self.v_abs)

		else : 
			self.r_abs, self.v_abs = self.r_cr, self.v_cr 
			self.r_abs_norm, self.v_abs_norm = self.r_cr_norm, self.v_cr_norm


	def Helio2Planeto (self, body) : 

		new_r = self.rotation_matrix.dot(body.r_cr - self.r_abs)
		new_v = self.rotation_matrix.dot(body.v_cr - self.v_abs)

		return new_r, new_v

	def Planeto2Helio (self, body) : 

		new_r = self.inv_rotation_matrix.dot(body.r_cr) + self.r_abs
		new_v = self.inv_rotation_matrix.dot(body.v_cr) + self.v_abs

		return new_r, new_v

	def Planeto2NatSat (self, body) : 

		new_r = body.r_cr - self.r_cr
		new_v = body.v_cr - self.v_cr

		return new_r, new_v 

	def NatSat2Planeto (self, body) : 

		new_r = body.r_cr + self.r_cr
		new_v = body.v_cr + self.v_cr

		return new_r, new_v

# eps = 0.4090928
# a0 = -1.5708
# d0 = 1.5708

# R_e = np.array([  [1.               ,                   0.,                   0.],
# 			              [0.               ,  math.cos(-eps), -math.sin(-eps)],
# 			              [0.,  math.sin(-eps),  math.cos(-eps)] ])

# R_a0 = np.array([ [ math.cos(a0),   math.sin(a0),                   0.],
# 			              [-math.sin(a0), math.cos(-a0),                   0.],
# 			              [0.                ,                  0.,                    1] ])

# R_d0 = np.array([ [1.                ,                  0.,                   0.],
# 			              [0.                ,   math.cos(d0),   -math.sin(d0)],
# 			              [0.                ,   math.sin(d0),    math.cos(d0)] ])

# t = np.array([1e3, 2e2, 3e6])
# print("-----")
# print(np.linalg.norm(t))
# t = np.linalg.inv(R_e).dot(R_a0.dot(R_d0.dot(t)))
# print(np.linalg.norm(t))
# print("-----")