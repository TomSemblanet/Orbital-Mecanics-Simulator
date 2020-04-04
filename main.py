# @autor : SEMBLANET Tom (ISAE-SUPAERO)

import matplotlib.animation as animation
import matplotlib.pyplot as plt

import parameters as prm
import utility_functions as u_f
import graphic_display as g_d
import gross_calculation as g_c


satellites_list, celestial_bodies_list = u_f.loadSimulation()

# g_c.GeneralCalculation(satellites_list, celestial_bodies_list)


if('Spatial View' in prm.parameters["applications"]["applications on"]) :
	space_displayer = g_d.MainDisplay(satellites_list, celestial_bodies_list)
	space_ani = animation.FuncAnimation(fig=space_displayer.figure, func=space_displayer.update, interval=1,  blit=False)

if('Ground Track' in prm.parameters["applications"]["applications on"]) : 
	ground_track_displayer = g_d.GroundTrackDisplay(satellites_list, celestial_bodies_list)
	ground_track_ani = animation.FuncAnimation(fig=ground_track_displayer.figure, func=ground_track_displayer.update, interval=1, blit=True)

if('Parameters Plot' in prm.parameters["applications"]["applications on"]) : 
	parameters_displayer = g_d.GraphDisplay(satellites_list, celestial_bodies_list)
	parameters_ani = animation.FuncAnimation(fig=parameters_displayer.figure, func=parameters_displayer.update, interval=1, blit=False)


plt.show()