import numpy as np 
import math 
import matplotlib.pyplot as plt

import satellite as sat 
import celestial_body as c_b 
import utility_functions as u_f 
import parameters as prm


import time



def GeneralCalculation () :

	satellites_list = sat.Satellite.satellites
	celestial_bodies_list = c_b.CelestialBody.celestial_bodies

	requested_bodies_names = ['SAT1']
	requested_bodies = [body for body in np.concatenate((satellites_list, celestial_bodies_list)) if body.name in requested_bodies_names]

	requested_attributes_names = ['a', 'e', 'i', 'Lnode', 'Lperi']

	dictionnary = dict()

	dictionnary['time steps'] = list()

	for body_name in requested_bodies_names : 
		dictionnary[body_name] = dict()

		for attr_name in ['r_cr', 'v_cr', 'r_abs', 'v_abs'] : 
			dictionnary[body_name][attr_name] = np.array([[]])

		for attr_name in requested_attributes_names : 
			dictionnary[body_name][attr_name] = np.array([])

	n_tour = 0

	start = time.time()

	while(prm.parameters['time']['elapsed time'] < prm.parameters['time']['simulation time']) : 

		n_tour += 1

		dictionnary['time steps'].append(prm.parameters['time']['elapsed time'])
		u_f.Computation()

		for body in requested_bodies : 

			for attr_name in ['r_cr', 'v_cr', 'r_abs', 'v_abs'] : 
				dictionnary[body.name][attr_name] = np.append(dictionnary[body.name][attr_name], getattr(body, attr_name))
				dictionnary[body.name][attr_name] = np.reshape(dictionnary[body.name][attr_name], (n_tour, 3))

			for attr_name in requested_attributes_names : 
				dictionnary[body.name][attr_name] = np.append(dictionnary[body.name][attr_name], getattr(body.orbit, attr_name))

	end = time.time()
	file_ = open('file.txt', 'w')
	file_.write(str(end-start))
		

	# plt.style.use('dark_background')
	# fig, ax = plt.subplots()
	# ax.plot(dictionnary['time steps'], dictionnary['SAT1']['Lperi']*180/math.pi)
	# plt.show()