import numpy as np
import matplotlib.pyplot as plt
import os
import math
from scipy.optimize import fsolve

import satellite as sat
import celestial_body as c_b
import parameters as prm
from datetime import datetime
import numerical_integration as n_i
import constants as cst

import sys, json


#################################################
#
# DESCRIPTION : increments the timer after each iteration
#
#################################################

def update_date () : 

	prm.parameters["time"]["elapsed time"] += prm.parameters["time"]["time step"]

	prm.parameters["time"]["current date"] = str(datetime.fromtimestamp(946724400+prm.parameters["time"]["initial julian date"]*86400+prm.parameters["time"]["elapsed time"]))[:23]
	open('file.txt', 'w').write(str(int(prm.parameters["time"]["current date"][11:13])))
	# prm["time"]["current_julian_date"] = 367*int(prm.parameters["time"]["current date"][0:4]) - int((7*(int(prm.parameters["time"]["current date"][0:4]) \
	# 				+ int((int(prm.parameters["time"]["current date"][5:7])+9)/12)))/4) \
	# 				+ int(275*int(prm.parameters["time"]["current date"][5:7])/9) + int(prm.parameters["time"]["current date"][8:10]) + 1721013.5 \
	# 				+ (((int(prm.parameters["time"]["current date"][17:19])/60) \
	# 				+ int(prm.parameters["time"]["current date"][14:16]))/60+int(prm.parameters["time"]["current date"][11:13]))/24 - 2451545 \


	if(prm.parameters["time"]["time step"] == 0) : 
		prm.parameters["time"]["time step"] = prm.parameters["time"]["general time step"]
		


def Computation () :

	# if(prm.parameters["applications"]["show bodies data"] == True) : 	
	# 	display_parameters([sat for sat in sat.Satellite.satellites if sat.name in prm.parameters["applications"]["bodies data displayed"]]+\
	# 		[cel_body for cel_body in c_b.CelestialBody.celestial_bodies if cel_body.name in prm.parameters["applications"]["bodies data displayed"]])

	# for i in range (prm.parameters["applications"]["calculation repeat"]) :  # repetition allow the program to reduce the computational time by reducing the number of plot
	update_celestial_bodies_position()
	satellites_accelerations()
	update_ref_body()
	update_date() 


def loadSimulation (parameters_dict) : 


	generals_prm = parameters_dict["general"]
	time_prm = parameters_dict["time"]

	satellites_prm = parameters_dict["satellites"]
	celestial_bodies_prm = parameters_dict["celestial bodies"]
	maneuvers_prm = parameters_dict["maneuvers"]

	# with open('file.txt', 'w') as file : 
	# 	file.write(json.dumps(generals_prm))
	# 	file.write('\n')
	# 	file.write(json.dumps(time_prm))
	# 	file.write('\n')
	# 	file.write(json.dumps(satellites_prm))
	# 	file.write('\n')
	# 	file.write(json.dumps(celestial_bodies_prm))
	# 	file.write('\n')
	# 	file.write(json.dumps(maneuvers_prm))
	# 	file.write('\n')


	# prm.parametersLoader()
	# load_celestial_bodies(prm.celestialBodiesLoader())
	# load_satellites(prm.satellitesLoader())
	# load_manoeuvers(prm.maneuverLoader())

	prm.generalParametersLoader(generals_prm)
	prm.timeParametersLoader(time_prm)
	load_celestial_bodies(celestial_bodies_prm)
	load_satellites(satellites_prm)
	load_manoeuvers(maneuvers_prm)


#################################################
#
# DESCRIPTION : displays the orbital parameters of all bodies given into argument (satellite and celestial bodies)
#				the display of these parameters slows down the simulation !
#
#################################################

def display_parameters (bodies) :

	os.system("clear")

	print(prm.parameters["time"]["current date"])
	print("-----------------------\n")
	print("Elapsed time : {} sec\n".format(round(prm.parameters["time"]["elapsed time"])))

	for body in bodies : 
		print(body)


def load_satellites (satellites_data_dicts) : 

	""" 
	Loads the real satellites objects given a list of dictionnaries containing the parameters needed to
	instanciate the satellites which has to be simulated

	Input : a list of dictionnaries containing the parameters needed to instanciate the satellites which has to be simulated

	"""	

	satellites_list = []

	for satellite_dict in satellites_data_dicts :

		for key, val in satellite_dict.items() : 
			if(str(type(val))=="<class 'list'>") :
				satellite_dict[key]=np.array(val)

		satellite_dict["corps_ref"] = [body for body in c_b.CelestialBody.celestial_bodies if body.name==satellite_dict["corps_ref"]][0]
		new_satellite = sat.Satellite(**satellite_dict)
		sat.Satellite.satellites.append(new_satellite)


def load_celestial_bodies (celestial_bodies_to_compute) : 

	""" 
	Loads the real celestial body objects given the list of the names of the celestial bodies which has 
	to be simulated

	Input : a list containing the names of the celestial bodies which has to be simulated

	"""	

	cst.Celestial_Bodies_Dict[celestial_bodies_to_compute["to load"][0]]['central'] = True

	for celestial_body_name in celestial_bodies_to_compute["to load"] :

		if(celestial_body_name == 'Sun') :
			new_celestial_body = c_b.CelestialBody(celestial_body_name)
		else : 
			new_celestial_body = c_b.CelestialBody(celestial_body_name, \
												   [cel_body for cel_body in c_b.CelestialBody.celestial_bodies if (cel_body.name == cst.Celestial_Bodies_Dict[celestial_body_name]["corps ref"])][0])

		# try : 
		# 	new_celestial_body = c_b.CelestialBody(celestial_body_name, \
		# 										   [cel_body for cel_body in c_b.CelestialBody.celestial_bodies if (cel_body.name == cst.Celestial_Bodies_Dict[celestial_body_name]["corps ref"])][0])
		# except : 
		# 	print(celestial_body_name)
		# 	input()
		# 	new_celestial_body = c_b.CelestialBody(celestial_body_name)

		c_b.CelestialBody.celestial_bodies.append(new_celestial_body)



def load_manoeuvers (maneuvers_dicts) :

	""" 
	Loads the real maneuver objects given a list of dictionnaries containing the parameters needed to
	instanciate the maneuvers which has to be assigned to the satellites

	Input : a list of dictionnaries containing the parameters needed to instanciate the maneuvers which has to assigned 
	to the satellites

	Return : a list containing the instantiated maneuvers objects 

	"""	

	satellites_dict = {}
	for sat_ in sat.Satellite.satellites :
		sat_.load_manoeuvers_list([man for man in maneuvers_dicts if man["sat_name"]==sat_.name]) 


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

def update_celestial_bodies_position () : 

	for celestial_body in c_b.CelestialBody.celestial_bodies[1:] : 
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

def update_ref_body () : 

	for satellite in sat.Satellite.satellites : 
		satellite.update_ref_body(c_b.CelestialBody.celestial_bodies)


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

def satellites_accelerations () :

	for satellite in sat.Satellite.satellites : 
		fire_on = False 
		if(satellite.current_maneuver is not None) : 
			fire_on = satellite.current_maneuver.trigger_detector.TriggerTimeSupervisor()
			if(fire_on == True) : 
				satellite.current_maneuver.data_loader(satellite.current_maneuver)
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
	return np.sign(np.cross(body1.r_cr, body2.r_cr)[2]) * math.acos( np.dot(body1.r_cr, body2.r_cr)/(body1.r_cr_norm*body2.r_cr_norm) )


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

	# flight_time -= prm.dT # il faut enlever prm.dT au temps de vol car il se passe un tour de boucle le temps que le satellite adapte sa vitesse
	r_init_norm = np.linalg.norm(r_init)
	r_final_norm = np.linalg.norm(r_final)

	dPhi = math.acos(np.dot(r_init, r_final)/(r_init_norm*r_final_norm))

	if( ( np.dot(np.cross(r_init, r_final), [0, 0, 1]) < 0 and prograde ) or 
		( np.dot(np.cross(r_init, r_final), [0, 0, 1]) >= 0 and not prograde )) : 
		dPhi = 2*math.pi - dPhi

	temp = math.sin(dPhi)*math.sqrt(r_init_norm*r_final_norm/(1-math.cos(dPhi)))

	try :
		z = fsolve(NewtonRaphsonLambertFunction, args=(r_init_norm, r_final_norm, temp, flight_time, mu), x0=1)
	except : 
		print("> Unsolvable Lambert's Problem.")
		exit()

	Cz = (1 - math.cos(math.sqrt(z)))/z
	Sz = (math.sqrt(z)-math.sin(math.sqrt(z)))/(math.sqrt(z)**3)

	Yz = r_init_norm + r_final_norm + temp*(z*Sz-1)/math.sqrt(Cz)

	f = 1 - Yz/r_init_norm
	g = temp*math.sqrt(Yz/mu)
	gdot = 1 - Yz/r_final_norm

	v_init = (r_final - f*r_init)/g
	v_final = (gdot * r_final - r_init)/g


	return v_init 

def NewtonRaphsonLambertFunction (z, r_init_norm, r_final_norm, temp, flight_time, mu) : 

	Cz = (1 - math.cos(math.sqrt(z)))/z
	Sz = (math.sqrt(z)-math.sin(math.sqrt(z)))/(math.sqrt(z)**3)

	Yz = r_init_norm + r_final_norm + temp*(z*Sz-1)/math.sqrt(Cz)

	return ((Yz/Cz)**(1.5))*Sz + temp*math.sqrt(Yz)-math.sqrt(mu)*flight_time


def CartesianToKeplerian (r, v, mu, all=False) : 

	# file = open('file.txt', 'w')
	# file.write(str(type(r)))
	# file.write(str(type(v)))
	# file.write(str(type(mu)))

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

	e = 1/mu*(float((v_norm*v_norm - mu/r_norm))*r - float(r_norm*w_norm)*v)
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
		
	return (prm.parameters["time"]["elapsed time"] + Dt)



def CoordinatesPredictor (body, time) : 

	true_anomaly = AnglePredictor(body, time)
	state_vector = KeplerianToCartesian(body.orbit.a, body.orbit.e, body.orbit.i, body.orbit.Lperi, body.orbit.Lnode, true_anomaly, body.corps_ref.mu)

	return state_vector


def DateToSeconds (date1, date2) : 
	
	object_date1 = datetime.strptime(date1, "%Y-%m-%d %H:%M:%S.%f")
	object_date2 = datetime.strptime(date2, "%Y-%m-%d %H:%M:%S.%f")

	return (object_date2-object_date1).total_seconds()



def EquatorialToEcliptic (vector) : 

	"""
	Rotate a vector from the Equatorial referential to the Ecliptic one

	"""

	ecliptic_obliquity = 0.4090928
	R = np.array([ [1.,               0.,               0.],
			        [0.,      math.cos(ecliptic_obliquity),     -math.sin(ecliptic_obliquity)],
			        [0.,      math.sin(ecliptic_obliquity),      math.cos(ecliptic_obliquity)] ])

	return R.dot(vector)


def Ecliptic_Equatorial (vector, ec2eq) : 

	"""
	Rotate a vector from the Ecliptic referential to the Equatorial one
	
	"""


	if(ec2eq == True) : sign = -1
	else : sign = 1

	ecliptic_obliquity = 0.4090928
	R = np.array([ [1.,               0.,               0.],
			        [0.,      math.cos(sign*ecliptic_obliquity),     -math.sin(sign*ecliptic_obliquity)],
			        [0.,      math.sin(sign*ecliptic_obliquity),      math.cos(sign*ecliptic_obliquity)] ])

	return R.dot(vector)



