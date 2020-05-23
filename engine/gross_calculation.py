import numpy as np 
import math 
import matplotlib.pyplot as plt
import json

import satellite as sat 
import celestial_body as c_b 
import utility_functions as u_f 
import parameters as prm


import time

# Permet la convertion entre le "language" abrégé du moteur de calcul et le "language" intelligible employé
#	par l'UI
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

		"longitude": "Longitude",
		"latitude": "Latitude"
		} 


def GeneralCalculation (exploitation_dict) :

	open("verif.txt", 'a').write("\n\nLancement des calculs ...")

	satellites_list = sat.Satellite.satellites
	celestial_bodies_list = c_b.CelestialBody.celestial_bodies

	requested_bodies_names = [body.name for body in satellites_list] 
	requested_bodies = [body for body in np.concatenate((satellites_list, celestial_bodies_list)) if body.name in requested_bodies_names]

	position_attributes_names = ["r_cr", "v_cr", "r_abs", "v_abs"] # contient les paramètres à récupérer nécessairement 
	orbit_attributes_names = [] # contient les paramètres optionnels que peut demander l'utilisateur
	optional_position_attributes_name = [] # contient les paramètres optionnels que peut demander l'utilisateur

	inv_conv_table = {v: k for k, v in conv_table.items()} # inversion du dictionnaire conv_table

	# Remplissage des tableaux contenant les paramètres optionnels pour - par la suite - demander au moteur de calcul de les stocker
	#		en vue de les renvoyer par la suite à l'UI  ~> hormis les paramètres de position, les paramètres orbitaux, de distance etc...
	#		doivent être demandé par l'utilisateur pour être renvoyés pour éviter des variables trop lourdes
	for key_ in exploitation_dict["graphics"]["values"]  :
		translated_key = inv_conv_table[key_]

		if(translated_key in ["a", "e", "i", "Lnode", "Lperi"]) : # distinction entre les paramètres orbitaux à proprement parlé et les autres : distance, vitesse
																  # longitude, laitude ... car les premiers ne sont pas attributs de la classe Satellite mais de la classe Orbite
			orbit_attributes_names.append(translated_key)
		else : 
			optional_position_attributes_name.append(translated_key)

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


	# Remplacement des tableaux de tableaux ('r_cr', 'v_cr' ...) en uniques tableaux, beaucoup plus simple à traiter par la
	#		suite en Javascript sans numpy
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

	# Reconversion du language moteur au language intelligible en vue de renvoyer les résultats à l'UI
	dictionnary = dictTreatement(dictionnary, requested_bodies_names, (["x_cr", "y_cr", "z_cr", "vx_cr", "vy_cr", "vz_cr", "x_abs", "y_abs", "z_abs", "vx_abs", \
																			"vy_abs", "vz_abs"]+orbit_attributes_names+optional_position_attributes_name))

	open("verif.txt", 'a').write("\n\nFin des calculs ...")
	open("verif.txt", 'a').write(str(dictionnary))
	return dictionnary

def dictTreatement (dictionnary, requested_bodies_names, requested_attr) :

	for body_name in requested_bodies_names :
		for key in requested_attr  :
			dictionnary[body_name][conv_table[key]] = dictionnary[body_name][key]
			del dictionnary[body_name][key]

	return dictionnary

	