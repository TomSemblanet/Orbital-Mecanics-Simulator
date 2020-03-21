# @autor : SEMBLANET Tom (ISAE-SUPAERO)


import numpy as np 
import matplotlib.pyplot as plt
import math

import satellite as sat
import celestial_body as c_b
import constants as cst
import parameters as prm
import utility_functions as u_f
import graphic_display as g_d
import maneuver 
import matplotlib.animation as animation


									   	################ - INITIALISATION OF CELESTIAL BODIES - ################

celestial_bodies_list = u_f.load_celestial_bodies([
												   {
												   "name" : "Earth",
												   "r0" : np.array([0., 0., 0.]),
												   "v0" : np.array([0., 0., 0.])
												   },

												   {
												   "name" : "Moon",
												   "r0" : np.array([356700e3, 0., 0.]),
												   "v0" : np.array([0., 1052, 0.])
												   }
												  ])


										################## - INITIALISATION OF SATELLITE(S) - ##################


satellites_list = u_f.load_satellites( [ 
										{
										"name" : "SAT1",
										"r0" : np.array([-22000e3, 0, 0]),
										"v0" : np.array([0, -3000-0.1, 1000]),
										"corps_ref" : [body for body in celestial_bodies_list if body.name=="Earth"][0],
										"color" : "m"
										}, 

										{
										"name" : "SAT2",
										"r0" : np.array([-29000e3, 0, 0]),
										"v0" : np.array([0, -2000-0.1, 2000]),
										"corps_ref" : [body for body in celestial_bodies_list if body.name=="Earth"][0],
										"color" : "c"
										}
									   ] )


										################## - INITIALISATION OF MANEUVERS - ##################

u_f.load_manoeuvers(satellites_list, 
					[
						{
						"sat_name" : "SAT1",
						"man_name" : "apogee modification",
						"value" : 100e3,
						"trigger_type" : "true anomaly",
						"trigger_value" : 180,
						"direction" : None
						}
					]	
				    )

if(1 in prm.applicationsOn) :
	space_displayer = g_d.MainDisplay(satellites_list, celestial_bodies_list, display_mode="trajectory prediction", following_mode=False)
	space_ani = animation.FuncAnimation(fig=space_displayer.figure, func=space_displayer.update, interval=0, repeat=False, blit=False)

if(2 in prm.applicationsOn) : 
	ground_track_displayer = g_d.GroundTrackDisplay(satellites_list, celestial_bodies_list)
	ground_track_ani = animation.FuncAnimation(fig=ground_track_displayer.figure, func=ground_track_displayer.update, interval=0, repeat=False, blit=True)

if(3 in prm.applicationsOn) : 
	parameters_displayer = g_d.GraphDisplay(satellites_list, celestial_bodies_list, "Speed relative to referent body : SAT1 SAT2")
	parameters_ani = animation.FuncAnimation(fig=parameters_displayer.figure, func=parameters_displayer.update, interval=0, repeat=False, blit=False)

plt.show()





