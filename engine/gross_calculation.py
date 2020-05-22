import numpy as np 
import math 
import matplotlib.pyplot as plt
import json

import satellite as sat 
import celestial_body as c_b 
import utility_functions as u_f 
import parameters as prm


import time



def GeneralCalculation () :

	open("verif.txt", 'a').write("\n\nLancement des calculs ...")

	satellites_list = sat.Satellite.satellites
	celestial_bodies_list = c_b.CelestialBody.celestial_bodies

	requested_bodies_names = [body.name for body in satellites_list] 
	requested_bodies = [body for body in np.concatenate((satellites_list, celestial_bodies_list)) if body.name in requested_bodies_names]

	# requested_attributes_names = ["a", "e", "i", "Lnode", "Lperi", "true_anomaly"]
	# requested_orbit_attributes_names = ["a", "e", "i", "Lnode", "Lperi"]
	# requested_attitude_attributes_names = ["r_cr", "v_cr", "r_abs", "v_abs", "true_anomaly"]

	position_attributes_names = ["r_cr", "v_cr", "r_abs", "v_abs"]
	orbit_attributes_names = ["a", "e", "i", "Lnode", "Lperi"]
	optional_position_attributes_name = ["r_cr_norm", "v_cr_norm", "r_abs_norm", "v_abs_norm", "true_anomaly"]
	

	dictionnary = dict()

	dictionnary["time steps"] = list()

	for body_name in requested_bodies_names : 
		dictionnary[body_name] = dict()

		for attr_name in position_attributes_names : 
			dictionnary[body_name][attr_name] = np.array([[]])

		for attr_name in np.concatenate((orbit_attributes_names, optional_position_attributes_name)) : 
			dictionnary[body_name][attr_name] = np.array([])

	n_tour = 0

	start = time.time()

	while(prm.parameters["time"]["elapsed time"] < prm.parameters["time"]["simulation time"]) : 

		n_tour += 1

		dictionnary["time steps"].append(prm.parameters["time"]["elapsed time"])
		u_f.Computation()

		for body in requested_bodies : 

			for attr_name in position_attributes_names : 
				dictionnary[body.name][attr_name] = np.append(dictionnary[body.name][attr_name], getattr(body, attr_name))
				dictionnary[body.name][attr_name] = np.reshape(dictionnary[body.name][attr_name], (n_tour, 3))

			for attr_name in orbit_attributes_names : 
				dictionnary[body.name][attr_name] = np.append(dictionnary[body.name][attr_name], getattr(body.orbit, attr_name))

			for attr_name in optional_position_attributes_name : 
				dictionnary[body.name][attr_name] = np.append(dictionnary[body.name][attr_name], getattr(body, attr_name))

			# dictionnary[body.name]['true_anomaly'] = np.append(dictionnary[body.name]['true_anomaly'], getattr(body, 'true_anomaly'))


	for body in requested_bodies : 
		dictionnary[body.name]["x_cr"] = [x[0] for x in dictionnary[body.name]["r_cr"]]
		dictionnary[body.name]["y_cr"] = [x[1] for x in dictionnary[body.name]["r_cr"]]
		dictionnary[body.name]["z_cr"] = [x[2] for x in dictionnary[body.name]["r_cr"]]
		del dictionnary[body.name]["r_cr"]

		dictionnary[body.name]["vx_cr"] = [x[0] for x in dictionnary[body.name]["v_cr"]]
		dictionnary[body.name]["vy_cr"] = [x[1] for x in dictionnary[body.name]["v_cr"]]
		dictionnary[body.name]["vz_cr"] = [x[2] for x in dictionnary[body.name]["v_cr"]]
		del dictionnary[body.name]["v_cr"]

		dictionnary[body.name]["x_abs"] = [x[0] for x in dictionnary[body.name]["r_abs"]]
		dictionnary[body.name]["y_abs"] = [x[1] for x in dictionnary[body.name]["r_abs"]]
		dictionnary[body.name]["z_abs"] = [x[2] for x in dictionnary[body.name]["r_abs"]]
		del dictionnary[body.name]["r_abs"]

		dictionnary[body.name]["vx_abs"] = [x[0] for x in dictionnary[body.name]["v_abs"]]
		dictionnary[body.name]["vy_abs"] = [x[1] for x in dictionnary[body.name]["v_abs"]]
		dictionnary[body.name]["vz_abs"] = [x[2] for x in dictionnary[body.name]["v_abs"]]
		del dictionnary[body.name]["v_abs"]

	# conversion des ndarray (type propre à numpy non supporté par le format .json) en tableaux classiques
	for body_name in requested_bodies_names : 
		for key, value in dictionnary[body_name].items() : 
			if( str(type(dictionnary[body_name][key])) == "<class 'numpy.ndarray'>" ) : 
				dictionnary[body_name][key] = list(dictionnary[body_name][key])

				for ind, elmt in enumerate(dictionnary[body_name][key]) : 
					if( str(type(dictionnary[body_name][key][ind])) == "<class 'numpy.ndarray'>" ) : 
						dictionnary[body_name][key][ind] = list(dictionnary[body_name][key][ind])

	dictionnary = dictTreatement(dictionnary, requested_bodies_names)

	open("verif.txt", 'a').write("\n\nFin des calculs ...")
	open("verif.txt", 'a').write(str(dictionnary))
	return dictionnary

def dictTreatement (dictionnary, requested_bodies_names) :

	conv_table = {
		"a": "Demi grand-axe",
		"e": "Excentricité",
		"i": "Inclinaison",
		"Lnode": "Longitude du noeud ascendant",
		"Lperi": "Argument du périgé",
		"true_anomaly": "Anomalie vraie",

		"x_cr": "x (planeto)",
		"y_cr": "y (planeto)",
		"z_cr": "z (planeto)",
		"vx_cr": "vx (planeto)",
		"vy_cr": "vy (planeto)",
		"vz_cr": "vz (planeto)",
		"r_cr_norm": "Distance (planeto)",
		"v_cr_norm": "Vitesse (planeto)",

		"x_abs": "x (absolu)",
		"y_abs": "y (absolu)",
		"z_abs": "z (absolu)",
		"vx_abs": "vx (absolu)",
		"vy_abs": "vy (absolu)",
		"vz_abs": "vz (absolu)",
		"r_abs_norm": "Distance (absolu)",
		"v_abs_norm": "Vitesse (absolu)",
		} 



	for body_name in requested_bodies_names :
		for key in conv_table.keys()  :
			dictionnary[body_name][conv_table[key]] = dictionnary[body_name][key]
			open("xx.txt", 'a').write(str(body_name) + " : " + str(key) + "\n" + str(dictionnary[body_name][conv_table[key]]) + '\n\n\n')
			del dictionnary[body_name][key]

	return dictionnary

	