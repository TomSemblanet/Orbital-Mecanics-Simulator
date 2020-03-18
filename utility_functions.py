import numpy as np
import matplotlib.pyplot as plt
import os
import math
from scipy.optimize import fsolve

import satellite as sat
import celestial_body as c_b
import constants as cst
import numerical_integration as n_i


#################################################
#
# DESCRIPTION : increments the timer after each iteration
#
#################################################

def update_date () : 
	cst.time += cst.H
	if(cst.H == 0) : 
		cst.H = cst.ideal_H


#################################################
#
# DESCRIPTION : displays the orbital parameters of all bodies given into argument (satellite and celestial bodies)
#				the display of these parameters slows down the simulation !
#
#################################################

def display_parameters (bodies) :

	os.system("clear")

	print("Time : {} sec\n".format(cst.time))

	for body in bodies : 
		print('> {}\n'.format(body.name))
		print('- Semi-major axis (a) : {} km'.format(round(body.orbit.a/1000, 0)))
		print('- Eccentricity (e) : {}'.format(round(body.orbit.e, 5)))
		print('- True anomaly : {} °'.format(round(body.true_anomaly*180/math.pi, 4)))
		print('- Longitude of perigee : {} °'.format(round(body.orbit.Lperi*180/math.pi, 2)))
		print('- Longitude of ascendant node : {} °'.format(round(body.orbit.Lnode*180/math.pi, 2)))
		print('- Inclinaison : {} °'.format(round(body.orbit.i*180/math.pi, 2)))
		print('- Period : {} sec'.format(round(body.orbit.T, 2)))
		print('- Distance : {} km'.format(round(body.r_cr_std/1000, 2)))
		print('- Velocity : {} km/s'.format(round(body.v_cr_std/1000, 2)))
		print('- Cartesian Coord : {}'.format(body.r_cr))
		print('- Cartesian Velocity : {}'.format(body.v_cr))
		print('- H : {}'.format(cst.H))
		print("\n\n")


#################################################
#
# DESCRIPTION : calls the constructors of each satellites 
#
#
# INPUT : 
#
# - satellites_data_list : 				5x1 array [-] : arguments to pass to the constructor of each satellites (initial position, initial velocity, name, referent body and color)
#
#
# OUTPUT : 
#
# - satellites_list : 				nx1 satellite_object array [-] : list of all constructed satellites returned by their own constructors
#
#################################################

def load_satellites (satellites_data_list) : 

	satellites_list = []

	for i in range (0, len(satellites_data_list)) :
		new_satellite = sat.Satellite(satellites_data_list[i][0], satellites_data_list[i][1], satellites_data_list[i][2], satellites_data_list[i][3], satellites_data_list[i][4])
		satellites_list.append(new_satellite)
	
	return satellites_list


#################################################
#
# DESCRIPTION : calls the functions which allow the load of the manoeuvers for each satellites
#
#
# INPUT : 
#
# - satellites_list : 				nx1 satellite_object array [-] : list containing all satellites 
# - manoeuvers_lists : 				nx1 manoeuvers_list array [-] : list containing all the manoeuvers for each satellites
#
#
#################################################

def load_manoeuvers (satellites_list, manoeuvers_lists) : 

	for i in range (0, len(manoeuvers_lists)) :	
		satellites_list[i].load_manoeuvers_list(manoeuvers_lists[i])


#################################################
#
# DESCRIPTION : calls the functions which update the position of each celestial bodies
#
#
# INPUT : 
#
# - celestial_bodies_list : 				nx1 celestial_body_object array [-] : list containing all the celestial bodies 
#
#################################################

def update_celestial_bodies_position (celestial_bodies_list) : 

	for celestial_body in celestial_bodies_list[1:] : 
		celestial_body.set_position()


#################################################
#
# DESCRIPTION : calls the functions which update the referent body for each satellites
#
#
# INPUT : 
#
# - satellites_list : 				nx1 satellite_object array [-] : list containing all the satellites
# - celestial_bodies_list :         mx1 celestial_body_object array [-] : list containing all the celestial bodies
#
#################################################

def update_ref_body (satellites_list, celestial_bodies_list) : 

	for satellite in satellites_list : 
		satellite.update_ref_body(celestial_bodies_list)


#################################################
#
# DESCRIPTION : calls the functions which compute the acceleration for each satellites
#
#
# INPUT : 
#
# - satellites_list : 				nx1 satellite_object array [-] : list containing all the satellites
# - celestial_bodies_list :         mx1 celestial_body_object array [-] : list containing all the celestial bodies
#
#################################################

# def satellites_accelerations (satellites_list, celestial_bodies_list) : 

# 	for satellite in satellites_list : 
# 		fire_on = satellite.fire_time_detection()
# 		if(fire_on == True) : satellite.compute_maneuver_parameters()
# 		satellite.acceleration_manager(fire_on)

def satellites_accelerations (satellites_list) :

	for satellite in satellites_list : 
		fire_on = False 
		if(satellite.current_maneuver is not None) : 
			fire_on = satellite.current_maneuver.trigger_detector.TriggerTimeSupervisor()
			if(fire_on == True) : satellite.current_maneuver.data_loader(satellite.current_maneuver)
		satellite.acceleration_manager(fire_on)


#################################################
#
# DESCRIPTION : computes the (oriented) angle between the body n°1 and the body n°2
#				if the sens is prograde and the body n°1 is in advance then the returned angle is negative, it's positive if the n°1 is late compared to the n°2
#				else if the sens is reprograde and the body n°1 is late then the returned angle is negative, it's positive if the n°1 is in advance compared to the n°2
#
#
# INPUT : 
#
# - body1 : 							satellite_object (or) celestial_body_object : body n°1
# - body2 : 							satellite_object (or) celestial_body_object : body n°2
#
#
# OUTPUT : 
#
# - oriented_angle : 					float [rad] : oriented angle B1.O.B2 where O is one of the focus of each bodies orbit
#
#################################################

def get_angle (body1, body2) : 
	return np.sign(np.cross(body1.r_cr, body2.r_cr)[2]) * math.acos( np.dot(body1.r_cr, body2.r_cr)/(body1.r_cr_std*body2.r_cr_std) )


#################################################
#
# DESCRIPTION : conversion UA ~> m
#
#
# INPUT : 
#
# - x :				float [UA] : value in UA
#
#
# OUTPUT : 
#
# - x_m : 					float [m] : value in m
#
#################################################

def UAtoM (x) :
	return 1.496e11*x

#################################################
#
# DESCRIPTION : conversion UA/day ~> m/s
#
#
# INPUT : 
#
# - v :				float [UA/day] : value in UA/day
#
#
# OUTPUT : 
#
# - v_ms : 					float [m/s] : value in m/s
#
#################################################

def UAdtoMs (v) : 
	return 1.731e6*v


def LambertProblem (r_init, r_final, flight_time, mu, prograde=True) : 

	# flight_time -= cst.H # il faut enlever cst.H au temps de vol car il se passe un tour de boucle le temps que le satellite adapte sa vitesse

	r_init_std = np.linalg.norm(r_init)
	r_final_std = np.linalg.norm(r_final)

	dPhi = math.acos(np.dot(r_init, r_final)/(r_init_std*r_final_std))

	if( ( np.dot(np.cross(r_init, r_final), [0, 0, 1]) < 0 and prograde ) or 
		( np.dot(np.cross(r_init, r_final), [0, 0, 1]) >= 0 and not prograde )) : 
		dPhi = 2*math.pi - dPhi

	temp = math.sin(dPhi)*math.sqrt(r_init_std*r_final_std/(1-math.cos(dPhi)))

	z = fsolve(NewtonRaphsonLambertFunction, args=(r_init_std, r_final_std, temp, flight_time, mu), x0=1)

	Cz = (1 - math.cos(math.sqrt(z)))/z
	Sz = (math.sqrt(z)-math.sin(math.sqrt(z)))/(math.sqrt(z)**3)

	Yz = r_init_std + r_final_std + temp*(z*Sz-1)/math.sqrt(Cz)

	f = 1 - Yz/r_init_std
	g = temp*math.sqrt(Yz/mu)
	gdot = 1 - Yz/r_final_std

	v_init = (r_final - f*r_init)/g
	v_final = (gdot * r_final - r_init)/g

	# print(r_init)
	# print(v_init)

	cst.r = r_init
	cst.v = v_init

	return v_init

def NewtonRaphsonLambertFunction (z, r_init_std, r_final_std, temp, flight_time, mu) : 

	Cz = (1 - math.cos(math.sqrt(z)))/z
	Sz = (math.sqrt(z)-math.sin(math.sqrt(z)))/(math.sqrt(z)**3)

	Yz = r_init_std + r_final_std + temp*(z*Sz-1)/math.sqrt(Cz)

	return ((Yz/Cz)**(1.5))*Sz + temp*math.sqrt(Yz)-math.sqrt(mu)*flight_time


def CartesianToKeplerian (r, v, mu, all=False) : 

	r_norm = np.linalg.norm(r)
	v_norm = np.linalg.norm(v)
	w_norm = np.dot(r, v)/r_norm

	h = np.cross(r, v)
	h_norm = np.linalg.norm(h)

	i = math.acos(h[2]/h_norm)

	n = np.cross([0, 0, 1], h)
	n_norm = np.linalg.norm(n)

	if(n_norm != 0) : 
		Lnode = math.acos(n[0]/n_norm)
		if(n[1] < 0) : 
			Lnode = 2*math.pi - Lnode
	else : 
		Lnode = 0

	e = 1/mu*((v_norm*v_norm - mu/r_norm)*r - r_norm*w_norm*v)
	e_norm = np.linalg.norm(e)

	if(n_norm != 0) : 
		if(e_norm > 1e-5) : 
			Lperi = math.acos(np.dot(n, e)/(n_norm*e_norm))
			if(e[2] < 0) : 
				Lperi = 2*math.pi - Lperi
		else : 
			Lperi = 0
	else : 
		Lperi = (math.atan2(e[1], e[0]))%(2*math.pi)
		if(np.sign(np.cross(r,v))[2] < 0) : 
			Lperi = 2*math.pi - Lperi

	if(e_norm > 1e-5) : 
		true_anomaly = math.acos(np.dot(e, r)/(e_norm*r_norm))
		if(w_norm < 0) : 
			true_anomaly = 2*math.pi - true_anomaly
	else : 
		true_anomaly = math.acos(np.dot(n, r)/(n_norm*r_norm))
		if(np.cross(n, r)[2] < 0) : 
			true_anomaly = 2*math.pi - true_anomaly

	a = h_norm*h_norm/(mu*(1-e_norm*e_norm))

	if(all) : 
		return (a, e_norm, i, Lnode, Lperi, true_anomaly, e, n, n_norm) 
	else :
		return (a, e_norm, i, Lnode, Lperi, true_anomaly)


def KeplerianToCartesian(a, e, i, Lperi, Lnode, true_anomaly, mu) : 

	h = math.sqrt(mu*a*(1-e**2))

	r_orbital_plan = (h*h/mu)*(1/(1+e*math.cos(true_anomaly)))*np.array([math.cos(true_anomaly), math.sin(true_anomaly), 0])
	v_orbital_plan = mu/h*np.array([-math.sin(true_anomaly), e+math.cos(true_anomaly), 0])


	R1 = np.array([ [math.cos(Lperi), -math.sin(Lperi), 0.],
			        [math.sin(Lperi),  math.cos(Lperi), 0.],
			        [             0.,               0., 1.] ])

	R2 = np.array([ [1.,               0.,               0.],
		            [0.,      math.cos(i),     -math.sin(i)],
		            [0.,      math.sin(i),      math.cos(i)] ])

	R3 = np.array([ [math.cos(Lnode), -math.sin(Lnode),     0.],
		            [math.sin(Lnode),  math.cos(Lnode),     0.],
		            [             0.,               0.,     1.] ])

	r = R3.dot(R2.dot(R1.dot(r_orbital_plan)))
	v = R3.dot(R2.dot(R1.dot(v_orbital_plan)))
	
	return np.concatenate((r, v))



def AnglePredictor (body, time) :  

	initial_E = 2*math.atan( math.sqrt((1-body.orbit.e)/(1+body.orbit.e)) * math.tan(body.true_anomaly/2))
	initial_M = initial_E - body.orbit.e*math.sin(initial_E)

	requested_M = initial_M + (2*math.pi/body.orbit.T)*time
	requested_E = requested_M

	delt = 1

	while(delt > 1e-6) : 
		new_E = requested_E - (requested_E - body.orbit.e*math.sin(requested_E) - requested_M)/(1 - body.orbit.e*math.cos(requested_E))
		delt = abs(new_E - requested_E)
		requested_E = new_E

	requested_true_anomaly = ( 2*math.atan( math.sqrt( (1+body.orbit.e)/(1-body.orbit.e) ) * math.tan(requested_E/2)) ) 

	return requested_true_anomaly


def PassageTimePredictor (body, angle) : 

		angle = angle*math.pi/180

		E1 = 2*math.atan(math.sqrt((1-body.orbit.e)/(1+body.orbit.e))*math.tan(angle/2))
		E0 = 2*math.atan(math.sqrt((1-body.orbit.e)/(1+body.orbit.e))*math.tan(body.true_anomaly/2))


		Dt = math.sqrt(body.orbit.a*body.orbit.a*body.orbit.a/body.corps_ref.mu)*( E1 - body.orbit.e*math.sin(E1) - E0 + body.orbit.e*math.sin(E0)) 

		if(Dt < 0) : 
			Dt = body.orbit.T + Dt
		
		return (cst.time + Dt)



def CoordinatesPredictor (body, time) : 

	true_anomaly = AnglePredictor(body, time)
	state_vector = KeplerianToCartesian(body.orbit.a, body.orbit.e, body.orbit.i, body.orbit.Lperi, body.orbit.Lnode, true_anomaly, body.corps_ref.mu)

	return state_vector




