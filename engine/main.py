# @autor : SEMBLANET Tom (ISAE-SUPAERO)

import matplotlib.animation as animation
import matplotlib.pyplot as plt
import sys, json

import utility_functions as u_f
import gross_calculation as g_c


# Instanciation des objets de la simulation & chargement des paramètres
u_f.loadSimulation(json.loads(sys.argv[1]))

# Boucles principale de calcul
dict_ = g_c.GeneralCalculation()

# Envoie des données à l'UI
print(json.dumps(dict_))






# if('Spatial View' in prm.parameters["applications"]["applications on"]) :
# 	space_displayer = g_d.MainDisplay()
# 	space_ani = animation.FuncAnimation(fig=space_displayer.figure, func=space_displayer.update, interval=1,  blit=False)

# if('Ground Track' in prm.parameters["applications"]["applications on"]) : 
# 	ground_track_displayer = g_d.GroundTrackDisplay()
# 	ground_track_ani = animation.FuncAnimation(fig=ground_track_displayer.figure, func=ground_track_displayer.update, interval=1, blit=True)

# if('Parameters Plot' in prm.parameters["applications"]["applications on"]) : 
# 	parameters_displayer = g_d.GraphDisplay()
# 	parameters_ani = animation.FuncAnimation(fig=parameters_displayer.figure, func=parameters_displayer.update, interval=1, blit=False)


# plt.show()