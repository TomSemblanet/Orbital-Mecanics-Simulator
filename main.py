# @autor : SEMBLANET Tom (ISAE-SUPAERO)

import matplotlib.animation as animation
import matplotlib.pyplot as plt

import parameters as prm
import utility_functions as u_f
import graphic_display as g_d
import gross_calculation as g_c
import celestial_body as c_b


u_f.loadSimulation()

# g_c.GeneralCalculation(satellites_list, celestial_bodies_list)


if('Spatial View' in prm.parameters["applications"]["applications on"]) :
	space_displayer = g_d.MainDisplay()
	space_ani = animation.FuncAnimation(fig=space_displayer.figure, func=space_displayer.update, interval=1,  blit=False)

if('Ground Track' in prm.parameters["applications"]["applications on"]) : 
	ground_track_displayer = g_d.GroundTrackDisplay()
	ground_track_ani = animation.FuncAnimation(fig=ground_track_displayer.figure, func=ground_track_displayer.update, interval=1, blit=True)

if('Parameters Plot' in prm.parameters["applications"]["applications on"]) : 
	parameters_displayer = g_d.GraphDisplay()
	parameters_ani = animation.FuncAnimation(fig=parameters_displayer.figure, func=parameters_displayer.update, interval=1, blit=False)


plt.show()