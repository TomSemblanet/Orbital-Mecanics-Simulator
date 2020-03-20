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

earth = c_b.CelestialBody(np.array([0., 0., 0.]), np.array([0., 0., 0.]), mass=cst.massTe, mu=cst.muTe, radius=cst.radTe, name="Earth", moving_body=False)
moon = c_b.CelestialBody(np.array([356700e3, 0., 0.]), np.array([0., 1052, 0.]), mass=cst.massLu, mu=cst.muLu, radius=cst.radLu, name="Moon", moving_body=True, corps_ref=earth)

# The body n°1 of the celestial_bodies_list has to be the "main" body (sun in an heliocentric referential, earth in a geocentric one ...)

celestial_bodies_list = [earth, moon]

										################ - INITIALISATION OF SATELLITE(S) PARAMETERS - ################


p = np.array([-22000e3, 0, 0])
v = np.array([0, -math.sqrt(cst.muTe/22000e3)-0.1, 1000])

satellites_list = u_f.load_satellites( [ [p, v, "S1", earth, "m"]] )

u_f.load_manoeuvers(satellites_list, 
					[ 
						[
						
						]
					]	
				    )

if(1 in prm.applicationsOn) :
	space_displayer = g_d.MainDisplay(satellites_list, celestial_bodies_list, display_mode="path", following_mode=True)
	space_ani = animation.FuncAnimation(fig=space_displayer.figure, func=space_displayer.update, interval=0, repeat=False, blit=False)

if(2 in prm.applicationsOn) : 
	ground_track_displayer = g_d.GroundTrackDisplay(satellites_list, celestial_bodies_list)
	ground_track_ani = animation.FuncAnimation(fig=ground_track_displayer.figure, func=ground_track_displayer.update, interval=0, repeat=False, blit=True)

# if(3 in prm.applicationsOn) : 
# 	parameters_displayer = g_d.GraphDisplay(...)
# 	parameters_ani = animation.FuncAnimation(fig=parameters_displayer.figure, func=parameters_displayer.update, interval=0, repeat=False, blit=False)

plt.show()





