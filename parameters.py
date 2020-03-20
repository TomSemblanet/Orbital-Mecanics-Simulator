import numpy as np

# Mathematical processing parameters (Burlisch Stoer Method)

jmax = 10
N = 6  
A = np.zeros((jmax+1, jmax+1, N))
m = 2*(np.arange(jmax+1)+1)
atol = 1e-12
rtol= 1e-5


# Time parameters

ideal_H = 10
H = ideal_H

starting_date = "2000/01/01 12:00:00" # [YYYY/MM/JJ HH:MM:SS]

initial_julian_date = 0. # [days]
current_julian_date = 0. # [days]

elapsed_time = 0. # [sec]


# General simulation parameters

simulation_speed_dict = {"slow" : 1, 
						"medium" : 2,
						"high" : 3,
						"very high" : 4}

simulation_speed = "medium"
calculation_repeat = simulation_speed_dict.get(simulation_speed)

applicationsOn = [1, 2]
leaderApplication = min(applicationsOn) # The leader application is the one which will call the calculation at each time step in order to be able
										# to display only the ground track or only the graphical parameters display ...


# MainDisplay parameters

parameters_on = True


# GroundTrackDisplay parameters




# GraphDisplay parameters



