import matplotlib.pyplot as plt
import numpy as np 
import math

import celestial_body as c_b
import constants as cst
import parameters as prm
import numerical_integration as n_i
import utility_functions as u_f
import orbit as orb
import maneuver


class Satellite : 

	#################################################
	#
	# DESCRIPTION : constructor of satellite objects, initialization of the parameters
	#
	#
	# INPUTS : 
	# 
	# - r0 :				3x1 float-array [m] : initial position of the satellite in the referentiel of its initial referent body
	# - v0 : 				3x1 float-array [m/s] : initial velocity of the satellite in the referentiel of its initial referent body
	# - name :              string [-] : name of the satellite
	# - corps_ref :         celestial_body_object [-] : celestial object around which the satellite initially orbits and around which it will orbit before the first exit of SOI (Sphere Of Influence)
	# - color : 			string [-] : plot color of the satellite
	#
	#
	# OUTPUTS : 
	#
	# - satellite :         satellite [object] : initialized satellite object
	#
	#################################################

	def __init__ (self, r0, v0, name, corps_ref, color="m") :

		self.name = name # name of the satellite
		self.color = color # color of the plot

		self.corps_ref = corps_ref # body around which the satellite initially orbits

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

		self.perigee_radius = 0.

		self.loadParameters(first_load=True)


	#################################################
	#
	# DESCRIPTION : calculates all the parameters of the satellite after an acceleration, a modification of SOI or at construction of the satellite.
	#				calculates rotations needed to go in the orbital plan from the referent body plan.
	#
	#################################################

	def loadParameters (self, first_load=False) :

		# Position and state vector 
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

		# Direction of the orbit
		self.movement_prograde = np.cross(self.r_cr, self.v_cr)[2] > 0

		# Angular momentum
		self.h = np.cross(self.r_cr, self.v_cr)
		self.h_std = np.linalg.norm(self.h)

		# True anomaly : setted in the orbitals parameters calculation (orbit constructor)
		self.initial_true_anomaly = self.true_anomaly

		self.longitude = (math.atan(self.r_cr[1]/self.r_cr[0]) + math.pi/2*(1-np.sign(self.r_cr[0]*1))) % (2*math.pi) - math.pi
		self.latitude = (math.atan(self.r_cr[2]/math.sqrt(self.r_cr[0]*self.r_cr[0]+self.r_cr[1]*self.r_cr[1])))

		self.perigee_radius = self.orbit.a*(1-self.orbit.e)


	#################################################
	#
	# DESCRIPTION : initalizes the list of manoeuvers that the satellite will have to follow in its attribut [self.manoeuvers_list]
	#
	#
	# INPUTS : 
	#
	# - manoeuvers_list :				nx1 array [-] : list of manoeuvers to load in the attribut [self.manoeuvers_list]
	#
	#################################################

	def load_manoeuvers_list (self, manoeuvers_list) : 

		self.manoeuvers_list = manoeuvers_list
		self.LoadNextManeuver()


	#################################################
	#
	# DESCRIPTION : load the next maneuver trigger following the wanted maneuver to be achieved
	#				the programm will then check if this trigger is reached or not at each time step
	#
	#################################################

	def LoadNextManeuver (self) : 

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


	#################################################
	#
	# DESCRIPTION : computes the acceleration of the satellite at each step following the Newton's laws and integrate the acceleration equation.
	#				only the attraction of the body whose satellite is in the SOI it taken into account, the integration also takes into account any acceleration 
	#				caused by a propulsion (to reache a given deltaV)
	#
	#
	# INPUTS : 
	#
	# - Y :				6x1 float-array [m, m, m, m/s, m/s, m/s] : state vector of the satellite before the acceleration, gives the information about its position and velocity
	# - t : 			time [sec] : time at the moment of acceleration
	#
	#
	# OUTPUTS : 
	#
	# - velocity/acceleration vector :         6x1 float-array [m/s, m/s, m/s, m/s^2, m/s^2, m/s^2] : return the velocity and acceleration computed by Newton's laws
	#
	#################################################

	def calculateAcceleration (self, Y, t, adapted_thrust=False) : 

		self.r_cr = np.array([ Y[0], Y[1], Y[2] ])
		self.r_abs = np.array([ Y[0], Y[1], Y[2] ]) + self.corps_ref.r_cr
		self.v_cr = np.array([ Y[3], Y[4], Y[5] ]) 
		self.v_abs = np.array([ Y[3], Y[4], Y[5] ]) + self.corps_ref.v_cr

		self.r_cr_std = np.linalg.norm(self.r_cr)
		self.r_abs_std = np.linalg.norm(self.r_abs)
		self.v_cr_std = np.linalg.norm(self.v_cr)
		self.v_abs_std = np.linalg.norm(self.v_abs) 

		# computation of the true anomaly taking into account the cases where e=0 (case [1] :  circular orbit) or/and where i=0 (case [2] : equatorial orbit)

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

		self.longitude = (math.atan(self.r_cr[1]/self.r_cr[0]) + math.pi/2*(1-np.sign(self.r_cr[0]*1)) - cst.wTe*prm.elapsed_time) % (2*math.pi) - math.pi
		self.latitude = (math.atan(self.r_cr[2]/math.sqrt(self.r_cr[0]*self.r_cr[0]+self.r_cr[1]*self.r_cr[1])))

		a =  (-self.corps_ref.mu)*(self.r_cr/(np.linalg.norm(self.r_cr)**3))



		#############################################
		#
		# Lorsque nous voulons un dV précis (par exemple pour une manoeuvre issue de
		# la résolution d'un problème de Lambert), il faut que le calcul du dV prenne
		# en compte l'accélération dut aux autres forces (frottements, gravité etc ...).
		# La prise en compte de ce dV peut se faire simplement en ajoutant à l'accélération
		# des boosters l'accélération qu'aurait normalement subit le satellite.
		#
		#############################################

		if(adapted_thrust) : 
			a = 0 # on fait comme si on annulait les autres forces via adaption de la propulsion des boosters, à modifier plus tard, peut-être afficher l'info ...

		if (self.thrust_acc_std != 0) :
			a += self.thrust_acc_vect*(self.thrust_acc_std)

		return (np.array([ Y[3], Y[4], Y[5], a[0], a[1], a[2] ]))


	def acceleration_manager (self, next_acceleration_on=False) : 


		if(next_acceleration_on == True) :

			prm.H = 1e-10

			self.thrust_acc_std = self.current_maneuver.maneuver_data.dV/prm.H
			self.thrust_acc_vect = self.current_maneuver.maneuver_data.direction
			if(np.linalg.norm(self.thrust_acc_vect) == 0) :
				self.thrust_acc_vect = self.v_cr/self.v_cr_std

			self.state_vector = n_i.burlirsch_stoer_method(self, prm.elapsed_time, prm.A, prm.N, self.state_vector, prm.m, adapted_thrust=True)
			self.thrust_acc_std = 0

			self.loadParameters()

			self.time_last_manoeuver = prm.elapsed_time
			self.LoadNextManeuver()

			prm.H = 0

		else : 
			self.state_vector = n_i.burlirsch_stoer_method(self, prm.elapsed_time, prm.A, prm.N, self.state_vector, prm.m)

	#################################################
	#
	# DESCRIPTION : updates the referent body of the satellite following the SOI approximation.
	#				if the satellite goes out of the SOI of a celestial body, it enters the SOI of the main celestial body (usually the Sun)
	#				at each modification of SOI (and so, of referent body) the parameters of the satellite and its trajectory are reloaded.
	#
	#
	# INPUT : 
	#
	# - celestial_bodies_list :			nx1 celestial_body_object array [-] : list of all the object whose satellite could possibly be in the sphere
	#
	#################################################

	def update_ref_body (self, celestial_bodies_list) :

		modified_corps_ref = False

		for body in celestial_bodies_list[1:] : 
			distance = np.linalg.norm( self.r_abs - body.r_abs )

			if(distance <= body.influence_sphere_radius and self.corps_ref != body) : 
				self.corps_ref = body
				modified_corps_ref = True
				break

		if(self.r_cr_std > self.corps_ref.influence_sphere_radius and self.corps_ref != celestial_bodies_list[0] and modified_corps_ref == False) : 
			self.corps_ref = celestial_bodies_list[0]
			modified_corps_ref = True

		if(modified_corps_ref == True) : 
			self.loadParameters()


	# Bruslisch Stoer's method function : doesn't need a description
	def pas_pointmilieu_modifie(self, H, t, Yn, m, adapted_thrust=False) :
		h = H/m
		u = Yn
		v = u+h*self.calculateAcceleration(u,t, adapted_thrust)
		for k in range(1,m):
			w = u+2*h*self.calculateAcceleration(v,t+k*h, adapted_thrust)
			u = v
			v = w

		return 0.5*(v+u+h*self.calculateAcceleration(v,t+H, adapted_thrust))
		







