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

	satellites_list = sat.Satellite.satellites
	celestial_bodies_list = c_b.CelestialBody.celestial_bodies

	requested_bodies_names = [body.name for body in satellites_list] 
	requested_bodies = [body for body in np.concatenate((satellites_list, celestial_bodies_list)) if body.name in requested_bodies_names]

	requested_attributes_names = ["a", "e", "i", "Lnode", "Lperi", "true_anomaly"]

	dictionnary = dict()

	dictionnary["time steps"] = list()

	for body_name in requested_bodies_names : 
		dictionnary[body_name] = dict()

		for attr_name in ["r_cr", "v_cr", "r_abs", "v_abs"] : 
			dictionnary[body_name][attr_name] = np.array([[]])

		for attr_name in requested_attributes_names : 
			dictionnary[body_name][attr_name] = np.array([])

	n_tour = 0

	start = time.time()

	while(prm.parameters["time"]["elapsed time"] < prm.parameters["time"]["simulation time"]) : 

		n_tour += 1

		dictionnary["time steps"].append(prm.parameters["time"]["elapsed time"])
		u_f.Computation()

		for body in requested_bodies : 

			for attr_name in ["r_cr", "v_cr", "r_abs", "v_abs"] : 
				dictionnary[body.name][attr_name] = np.append(dictionnary[body.name][attr_name], getattr(body, attr_name))
				dictionnary[body.name][attr_name] = np.reshape(dictionnary[body.name][attr_name], (n_tour, 3))

			for attr_name in requested_attributes_names[:-1] : # on ne prend pas l'anomalie vraie car ce n'est pas un attribut de la classe Orbite 
				dictionnary[body.name][attr_name] = np.append(dictionnary[body.name][attr_name], getattr(body.orbit, attr_name))

			dictionnary[body.name]['true_anomaly'] = np.append(dictionnary[body.name]['true_anomaly'], getattr(body, 'true_anomaly'))

	# conversion des ndarray (type propre à numpy non supporté par le format .json) en tableaux classiques
	for body_name in requested_bodies_names : 
		for key, value in dictionnary[body_name].items() : 
			if( str(type(dictionnary[body_name][key])) == "<class 'numpy.ndarray'>" ) : 
				dictionnary[body_name][key] = list(dictionnary[body_name][key])

				for ind, elmt in enumerate(dictionnary[body_name][key]) : 
					if( str(type(dictionnary[body_name][key][ind])) == "<class 'numpy.ndarray'>" ) : 
						dictionnary[body_name][key][ind] = list(dictionnary[body_name][key][ind])

	return dictionnary