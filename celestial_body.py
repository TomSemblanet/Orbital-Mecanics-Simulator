import matplotlib.pyplot as plt
import numpy as np 
import math

import parameters as prm
import constants as cst
import utility_functions as u_f
import orbit as orb


class CelestialBody : 


	#################################################
	#
	# DESCRIPTION : constructor of celestial body objects, initialization of the parameters
	#
	#
	# INPUTS : 
	#
	# - r0 :				3x1 float-array [m] : initial position of the body in the referentiel of its initial referent body
	# - v0 : 				3x1 float-array [m/s] : initial velocity of the body in the referentiel of its initial referent body
	# - mass : 				float [kg] : mass of the body
	# - mu : 				float [m^3/s^2] : standard gravitational parameter of the body
	# - radius : 			float [m] : radius of the body
	# - moving_body : 		boolean [-] : true if body is moving 
	# - name :              string [-] : name of the satellite
	# - corps_ref :         celestial_body_object [-] : celestial object around which the body initially orbits 
	#
	#
	# OUTPUTS : 
	#
	# - body :         celestial_body_object [-] : initialized celestial_body object
	#
	#################################################

	def __init__ (self, name) : 

		self.name = name
		self.color = "w"

		self.influence_sphere_radius = 0.
		self.mass = cst.Celestial_Bodies_Dict[self.name]["mass"]
		self.mu = cst.Celestial_Bodies_Dict[self.name]["mu"]
		self.radius = cst.Celestial_Bodies_Dict[self.name]["radius"]

		self.corps_ref_name = cst.Celestial_Bodies_Dict[self.name]["corps_ref"]
		self.corps_ref = None

		self.r_abs = cst.Celestial_Bodies_Dict[self.name]['initial_position']
		self.r_abs_std = np.linalg.norm(self.r_abs)

		self.r_cr = np.array([0., 0., 0.])
		self.r_cr_std = 0.
		
		self.v_abs = cst.Celestial_Bodies_Dict[self.name]['initial_velocity']
		self.v_abs_std = np.linalg.norm(self.v_abs)

		self.v_cr = np.array([0., 0., 0.])
		self.v_cr_std = 0.

		self.h_cr = np.array([0., 0., 0.])
		self.h_cr_std = 0.

		self.true_anomaly = 0.
		self.initial_true_anomaly = 0.

		self.E = 0.
		self.M = 0.

		self.moving_body = not(np.linalg.norm(self.r_abs) == 0)



	#################################################
	#
	# DESCRIPTION : calculates all the parameters of the celestial body at construction.
	#				calculates rotations needed to go in the orbital plan from the referent body plan.
	#
	#################################################

	def loadParameters (self, corps_ref) :

		self.corps_ref = corps_ref

		for i in [0, 1, 2] : 
			self.r_cr[i] = self.r_abs[i] - self.corps_ref.r_cr[i]
			self.v_cr[i] = self.v_abs[i] - self.corps_ref.v_cr[i]

		self.r_cr_std = np.linalg.norm(self.r_cr)
		self.v_cr_std = np.linalg.norm(self.v_cr)

		self.h_cr = np.cross(self.r_cr, self.v_cr)
		self.h_cr_std = np.linalg.norm(self.h_cr)

		self.orbit = orb.Orbit(self, self.r_cr, self.v_cr, self.corps_ref)

		self.influence_sphere_radius = self.orbit.a * (self.mass/self.corps_ref.mass)**(2/5)
		
		# True anomaly : setted in the orbitals parameters calculation (orbit constructor)
		self.initial_true_anomaly = self.true_anomaly

		self.E = 2*math.atan( math.sqrt((1-self.orbit.e)/(1+self.orbit.e)) *  math.tan(self.true_anomaly/2))
		self.M = self.E - self.orbit.e*math.sin(self.E)



	#################################################
	#
	# DESCRIPTION : computes the new position of the celestial body following Kepler's laws and by solving the Kepler's equation (Newton's method)
	#
	#################################################	

	def set_position (self) : 

		self.M = self.M + (2*math.pi/self.orbit.T)*prm.parameters["time"]["time step"]
		self.E = self.M

		delt = 1

		while(delt > 1e-6) : 
			new_E = self.E - (self.E - self.orbit.e*math.sin(self.E) - self.M)/(1 - self.orbit.e*math.cos(self.E))
			delt = abs(new_E - self.E)
			self.E = new_E

		self.true_anomaly = 2*math.atan( math.sqrt( (1+self.orbit.e)/(1-self.orbit.e) ) * math.tan(self.E/2))

		self.r_cr = self.orbit.R3.dot(self.orbit.R2.dot(self.orbit.R1.dot(np.array([self.orbit.a * (math.cos(self.E)-self.orbit.e), self.orbit.a * math.sqrt(1-self.orbit.e*self.orbit.e)*math.sin(self.E), 0]))))
		self.r_cr_std = np.linalg.norm(self.r_cr)

		self.v_cr = self.orbit.R3.dot(self.orbit.R2.dot(self.orbit.R1.dot(np.array([- math.sqrt( self.corps_ref.mu/(self.orbit.a*(1-self.orbit.e*self.orbit.e)) )*math.sin(self.true_anomaly), 
																  math.sqrt( self.corps_ref.mu/(self.orbit.a*(1-self.orbit.e*self.orbit.e)) )*(self.orbit.e+math.cos(self.true_anomaly)),
																  0.]))))

		self.v_cr_std = np.linalg.norm(self.v_cr)

		self.r_abs = self.r_cr + self.corps_ref.r_cr
		self.r_abs_std = np.linalg.norm(self.r_abs)

		self.v_abs = self.v_cr + self.corps_ref.v_cr
		self.v_abs_std = np.linalg.norm(self.v_abs)


