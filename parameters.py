import numpy as np
import datetime as dt

# Mathematical processing parameters (Burlisch Stoer Method)

jmax = 10
N = 6  
A = np.zeros((jmax+1, jmax+1, N))
m = 2*(np.arange(jmax+1)+1)
atol = 1e-12
rtol= 1e-5


# Time parameters

ideal_H = 1
H = ideal_H

starting_date = "2020-03-20 22:02:00" # [YYYY/MM/JJ HH:MM:SS]
current_date = ""

initial_julian_date = 367*int(starting_date[0:4]) - int((7*(int(starting_date[0:4])+int((int(starting_date[5:7])+9)/12)))/4) \
					+ int(275*int(starting_date[5:7])/9) + int(starting_date[8:10]) + 1721013.5 + (((int(starting_date[17:19])/60) \
					+ int(starting_date[14:16]))/60+int(starting_date[11:13]))/24 - 2451545 # [days]  following J2000
current_julian_date = 0. # [days]


elapsed_time = 0. # [sec]

# General simulation parameters

simulation_speed_dict = {"slow" : 1, 
						"medium" : 2,
						"high" : 3,
						"very high" : 4}

simulation_speed = "slow"
calculation_repeat = simulation_speed_dict.get(simulation_speed)

applicationsOn = [2]
leaderApplication = min(applicationsOn) # The leader application is the one which will call the calculation at each time step in order to be able
										# to display only the ground track or only the graphical parameters display ...


# MainDisplay parameters

parameters_on = True


# GroundTrackDisplay parameters




# GraphDisplay parameters



