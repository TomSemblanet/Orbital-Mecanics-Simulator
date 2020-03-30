import matplotlib.pyplot as plt
import numpy as np 
import math

import celestial_body as c_b
import constants as cst
import parameters as prm
import utility_functions as u_f
import orbit as orb
import maneuver

class Satellite : 

	def __init__ (self, r0, v0, name, corps_ref, color="m") :

		"""
		Constructor of the class Satellite. Initializes the attributs of each objects at creation before calling
		the loadParameters method that will compute other attributs (separate from the constructor because it's 
		called more than once during the simulation)

		Input : 
				- r0 : the initial position of the satellite in the referential of the body
							around which it orbits initially
				- v0 : the initial velocity of the satellite in the referential of the body
							around which it orbits initially
				- name : the name of the satellite
				- corps_ref : the body around which the body orbits initially
				- color : color of the satellite plot

		Return : None

		"""

		self.name = name
		self.color = color

		self.corps_ref = corps_ref

		self.r_cr = r0
		self.r_cr_std = np.linalg.norm(r0)

		self.v_cr = v0
		self.v_cr_std = np.linalg.norm(v0)

		self.h = np.array([0., 0., 0.])
		self.h_std = 0.

		self.state_vector = np.array([0., 0., 0., 0., 0., 0.])

		self.r_abs = np.array([0., 0., 0.])
		self.r_abs_std = 0.

		self.v_abs = np.array([0., 0., 0.])
		self.v_abs_std = 0.

		self.true_anomaly = 0.
		self.initial_true_anomaly = 0.
		
		self.thrust_acc_vect = np.array([ 0., 0., 0. ])
		self.thrust_acc_std = 0.

		self.longitude = 0.
		self.latitude = 0.

		self.movement_prograde = np.cross(self.r_cr, self.v_cr)[2] > 0

		self.manoeuvers_list = []
		self.current_maneuver = None
		self.next_manoeuver = -1
		self.time_last_manoeuver = 0.

		self.loadParameters(first_load=True)



	def __str__ (self) : 

		"""
		String method of the satellite class

		"""

		return '> {}\n'.format(self.name) + \
			   '- Semi-major axis (a) : {} km\n'.format(round(self.orbit.a/1000, 0)) + \
			   '- Eccentricity (e) : {}\n'.format(round(self.orbit.e, 5)) + \
			   '- True anomaly : {} °\n'.format(round(self.true_anomaly*180/math.pi, 4)) + \
			   '- Longitude of perigee : {} °\n'.format(round(self.orbit.Lperi*180/math.pi, 2)) + \
			   '- Longitude of ascendant node : {} °\n'.format(round(self.orbit.Lnode*180/math.pi, 2)) + \
			   '- Inclinaison : {} °\n'.format(round(self.orbit.i*180/math.pi, 2)) + \
			   '- Period : {} sec\n'.format(round(self.orbit.T, 2)) + \
			   '- Distance : {} km\n'.format(round(self.r_cr_std/1000, 2)) + \
			   '- Velocity : {} km/s\n'.format(round(self.v_cr_std)/1000, 2) + \
			   '- Cartesian Coord : {}\n'.format(self.r_cr) + \
			   '- Cartesian Velocity : {}\n'.format(self.v_cr) 



	def loadParameters (self, first_load=False) :

		"""
		Computes some additional attributes of the Satellite class and initializes the object orbit by calling
		its constructor. 
		This function has to be called each time the satellite orbital parameters change - to know :
			-	after each maneuver or change of sphere of influence in a Keplerian simulation
			-	at each time step in a non-Keplerian simulation

		Input : 
				- first_load : if True, the state vector in the absolute referential is computed from the state vector
							in the referent body referential.
							   if False, it's the opposite.

		Ouput : None

		"""

		if(first_load==True) : 
			for i in [0, 1, 2] : 
				self.r_abs[i] = self.r_cr[i] + self.corps_ref.r_cr[i]
				self.v_abs[i] = self.v_cr[i] + self.corps_ref.v_cr[i]

				self.state_vector[i] = self.r_cr[i]
				self.state_vector[i+3] = self.v_cr[i]

			self.r_abs_std = np.linalg.norm(self.r_abs)
			self.v_abs_std = np.linalg.norm(self.v_abs)

		else : 
			for i in [0, 1, 2] : 
				self.r_cr[i] = self.r_abs[i] - self.corps_ref.r_cr[i]
				self.v_cr[i] = self.v_abs[i] - self.corps_ref.v_cr[i]

				self.state_vector[i] = self.r_cr[i]
				self.state_vector[i+3] = self.v_cr[i]

			self.r_cr_std = np.linalg.norm(self.r_cr)
			self.v_cr_std = np.linalg.norm(self.v_cr)

		self.orbit = orb.Orbit(self, self.r_cr, self.v_cr, self.corps_ref)

		self.movement_prograde = np.cross(self.r_cr, self.v_cr)[2] > 0

		self.h = np.cross(self.r_cr, self.v_cr)
		self.h_std = np.linalg.norm(self.h)

		# True anomaly : setted in the orbitals parameters calculation (orbit constructor)
		self.initial_true_anomaly = self.true_anomaly

		self.longitude = (math.atan(self.r_cr[1]/self.r_cr[0]) + math.pi/2*(1-np.sign(self.r_cr[0]*1))) % (2*math.pi) - math.pi
		self.latitude = (math.atan(self.r_cr[2]/math.sqrt(self.r_cr[0]*self.r_cr[0]+self.r_cr[1]*self.r_cr[1])))


	def load_manoeuvers_list (self, manoeuvers_list) : 

		"""
		Loads the satellite list of dictionnaryr describing the maneuvers and calls the function LoadNextManeuver
		to instanciate the objects Maneuver

		Input : 
				- list of maneuvers dictionnaries

		Return : None

		"""

		self.manoeuvers_list = manoeuvers_list
		self.LoadNextManeuver()


	def LoadNextManeuver (self) : 

		"""
		Function called after each maneuver : loads the next maneuver to be triggered, instanciate the object and stores it
		in the attribut 'current_maneuver'

		Input : None

		Ouput : None

		"""

		self.next_manoeuver += 1
		if(self.next_manoeuver <= len(self.manoeuvers_list)-1) : 
			self.current_maneuver = maneuver.Maneuver(self, 
												  self.manoeuvers_list[self.next_manoeuver]["man_name"], 
												  self.manoeuvers_list[self.next_manoeuver]["value"],
												  self.manoeuvers_list[self.next_manoeuver]["trigger_type"],
												  self.manoeuvers_list[self.next_manoeuver]["trigger_value"],
												  self.manoeuvers_list[self.next_manoeuver]["direction"])

		else : 
			self.current_maneuver = None


	def RK4 (self, state_vector) :

		r = state_vector[:3]
		v = state_vector[3:]
		dt = prm.parameters['time']['time step']

		k1_r = v
		k1_v = self.calculateAcceleration(r)
	
		k2_r = v + k1_v*dt/2
		k2_v = self.calculateAcceleration(r + k1_r*dt/2)

		k3_r = v + k2_v*dt/2
		k3_v = self.calculateAcceleration(r + k2_r*dt/2)

		k4_r = v + k3_v*dt
		k4_v = self.calculateAcceleration(r + k3_r*dt)

		self.state_vector[:3] += dt/6*(k1_r + 2*k2_r + 2*k3_r + k4_r)
		self.state_vector[3:] += dt/6*(k1_v + 2*k2_v + 2*k3_v + k4_v)


	def calculateAcceleration (self, r, adapted_thrust=False) : 

		"""
		Computes the acceleration of the satellite at each step following the Newton's laws and integrate the acceleration equation.
		Only the attraction of the body whose satellite is in the SOI it taken into account, the integration also takes into account any acceleration 
		caused by a propulsion

		Input : 
				- Y : state vector of the satellite before the acceleration
				- t : elapsed time
				- adapted_thrust : if this parameter is set on True and the satellite is maneuvering, the propulsion will automatically adapted itself
								to nullify the other forces and so enhance the accuracy of the maneuver

		Return : 
				- the velocity and acceleration computed by Newton's laws

		"""

		if(adapted_thrust) : 
			acceleration = 0 
		else : 
			acceleration = (-self.corps_ref.mu/(np.linalg.norm(r)**3))*r

		if (self.thrust_acc_std != 0) :
			acceleration += self.thrust_acc_vect*(self.thrust_acc_std)

		return acceleration


	def updateParameters (self) : 

		self.r_cr = self.state_vector[:3]
		self.v_cr = self.state_vector[3:]
		self.r_abs = self.r_cr + self.corps_ref.r_abs
		self.v_abs = self.v_cr + self.corps_ref.v_abs

		self.r_cr_std = np.linalg.norm(self.r_cr)
		self.r_abs_std = np.linalg.norm(self.r_abs)
		self.v_cr_std = np.linalg.norm(self.v_cr)
		self.v_abs_std = np.linalg.norm(self.v_abs)

		if(self.orbit.e>5e-5) : # case [1]
			self.true_anomaly = math.acos(np.dot(self.orbit.ecc_vect, self.r_cr)/(self.orbit.e*self.r_cr_std)) % (2*math.pi)
			if(np.dot(self.r_cr, self.v_cr) < 0) :
				self.true_anomaly = 2*math.pi - self.true_anomaly

		elif(self.orbit.e<5e-5 and self.orbit.n_std != 0) : # case [2]
				self.true_anomaly = math.acos(np.dot(self.orbit.n, self.r_cr)/(self.orbit.n_std*self.r_cr_std)) % (2*math.pi)
				if(self.r_cr[2] < 0) : 
					self.true_anomaly = 2*math.pi - self.true_anomaly

		else :  # case [1]&[2]
			self.true_anomaly = math.acos(self.r_cr[0]/self.r_cr_std) % (2*math.pi)
			if(self.v_cr[0] > 0) : 
				self.true_anomaly = 2*math.pi -  self.true_anomaly

		self.longitude = (math.atan(self.r_cr[1]/self.r_cr[0]) + math.pi/2*(1-np.sign(self.r_cr[0]*1)) - cst.wTe*prm.parameters["time"]["elapsed time"]) % (2*math.pi) - math.pi
		self.latitude = (math.atan(self.r_cr[2]/math.sqrt(self.r_cr[0]*self.r_cr[0]+self.r_cr[1]*self.r_cr[1])))


	def acceleration_manager (self, next_acceleration_on=False) : 

		"""
		Manages maneuvers application : if the trigger of the pending maneuver is On, this function indicates to the calculateAcceleration
		method that the pending acceleration has to be taken into account in the computation of the satellite general acceleration.
		Also calls loadParameters method to recalculate the orbital parameters after the non-Keplerian acceleration and the loadNextManeuver
		method.

		Input : 
				- next_acceleration_on : indicates if the pending maneuver is triggered or not

		Output : None


		"""

		if(next_acceleration_on == True) :

			prm.parameters["time"]["time step"] = 1e-10

			self.thrust_acc_std = self.current_maneuver.maneuver_data.dV/prm.parameters["time"]["time step"]
			self.thrust_acc_vect = self.current_maneuver.maneuver_data.direction
			if(np.linalg.norm(self.thrust_acc_vect) == 0) :
				self.thrust_acc_vect = self.v_cr/self.v_cr_std
		
			self.RK4(self.state_vector)
			# self.state_vector = n_i.burlirsch_stoer_method(self, self.state_vector, adapted_thrust=True)
			self.thrust_acc_std = 0

			self.updateParameters()
			self.loadParameters()

			self.time_last_manoeuver = prm.parameters["time"]["elapsed time"]
			self.LoadNextManeuver()

			prm.parameters["time"]["time step"] = 0

		else : 
			self.RK4(self.state_vector)
			self.updateParameters()

	def update_ref_body (self, celestial_bodies_list) :

		"""
		Updates the referent body of the satellite following the SOI approximation.
    	if the satellite goes out of the SOI of a celestial body, it enters the SOI of the main celestial body (usually the Sun)
    	at each modification of SOI (and so of referent body) the parameters of the satellite and its trajectory are reloaded.

    	Input : 
    			- celestial_bodies_list : list of celestial bodiy objects

    	Return : None

		"""
		
		if (self.r_abs_std != self.r_cr_std) : # which means that the satellite is in the SOI of a planet

			if(self.r_cr_std > self.corps_ref.influence_sphere_radius) : 
				self.corps_ref = [body for body in celestial_bodies_list if body.name == self.corps_ref.corps_ref.name][0]
				self.loadParameters()

			else : 
				for natural_satellite in [body for body in celestial_bodies_list if body.name in cst.Celestial_Bodies_Dict[self.corps_ref.name]["natural satellites names"]] :
					distance = np.linalg.norm( self.r_abs - natural_satellite.r_abs )

					if(distance <= natural_satellite.influence_sphere_radius) :
						self.corps_ref = natural_satellite
						self.loadParameters()
						break

		else : 
			for body in celestial_bodies_list[1:] : 
				distance = np.linalg.norm( self.r_abs - body.r_abs )

				if(distance <= body.influence_sphere_radius) : 
					self.corps_ref = body
					self.loadParameters()
					break





