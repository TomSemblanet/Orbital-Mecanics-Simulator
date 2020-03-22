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

ideal_H = 5
H = ideal_H

starting_date = "2000-01-01 12:30:00.000" # [YYYY/MM/JJ HH:MM:SS]
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

applicationsOn = [1]
leaderApplication = min(applicationsOn) # The leader application is the one which will call the calculation at each time step in order to be able
										# to display only the ground track or only the graphical parameters display ...


# MainDisplay parameters

parameters_on = True


# GroundTrackDisplay parameters




# GraphDisplay parameters



def initialLoader () : 
	pass

def celestialBodiesLoader () :

	celestial_bodies_to_load = [] 

	with open("DATA.txt", 'r') as data_file : 

		begin_indice = 0
		lines = data_file.readlines()
		while (lines[begin_indice] != "========= CELESTIAL BODIES =========\n") : begin_indice+=1
		begin_indice+=2

		line = lines[begin_indice][2:]
		splited_line = line.split('] ')

		for l in splited_line[:-1] :
			if(l[-1] == 'v') : 
				celestial_bodies_to_load.append(l.split(' ')[0])

	return celestial_bodies_to_load


def satellitesLoader () : 

	dicts_to_send = []

	with open("DATA.txt", 'r') as data_file : 

		begin_indice, end_indice = 0, 0
		lines = data_file.readlines()

		while (lines[begin_indice] != "=========    SATELLITES    =========\n") : begin_indice+=1
		begin_indice+=2
		end_indice=begin_indice

		while (lines[end_indice] != "=========    MANEUVERS    =========\n") :	end_indice+=1
		end_indice-=2

		for line in lines[begin_indice:end_indice] : 
			splited_line = line.split('--')
			line_dict = dict()

			line_dict['name'] = splited_line[1].lstrip().replace(" ", "")

			string_tab = splited_line[2][1:-2]
			line_dict['r0'] = np.array([float(string_tab.split(',')[0].lstrip()), float(string_tab.split(',')[1].lstrip()), float(string_tab.split(',')[2].lstrip())])
			
			string_tab = splited_line[3][1:-2]
			line_dict['v0'] = np.array([float(string_tab.split(',')[0].lstrip()), float(string_tab.split(',')[1].lstrip()), float(string_tab.split(',')[2].lstrip())])
			
			line_dict['corps_ref'] = splited_line[4].replace(" ", "")
			
			line_dict['color'] = splited_line[5][:-1]

			dicts_to_send.append(line_dict)

	return dicts_to_send


def maneuverLoader () : 

	dicts_to_send = []

	with open("DATA.txt", 'r') as data_file : 

		begin_indice, end_indice = 0, 0
		lines = data_file.readlines()

		while (lines[begin_indice] != "=========    MANEUVERS    =========\n") : begin_indice+=1
		begin_indice+=2
		end_indice=begin_indice

		while (lines[end_indice] != "=========      TIME      =========\n") :	end_indice+=1
		end_indice-=2

		for line in lines[begin_indice:end_indice] : 
			print(">>>>>>>>>>>>>>")
			splited_line = line.split('--')
			line_dict = dict()

			line_dict['sat_name'] = splited_line[1][:-1]

			line_dict['man_name'] = splited_line[2][:-1]

			if(line_dict['man_name'] == "orbital rendez-vous") : 
				line_dict["value"] = dict()
				split = splited_line[3][:-1].replace("[", "").replace("]", "").replace(",", "").split(" ")
				line_dict["value"]["position_to_reach"] = np.array([float(split[0]), float(split[1]), float(split[2])])
				line_dict["value"]["date"] = float(split[3])
			else : 
				line_dict['value'] = float(splited_line[3][:-1])

			line_dict['trigger_type'] = splited_line[4][:-1]

			line_dict['trigger_value'] = float(splited_line[5][:-1])

			line_dict['direction'] = splited_line[6][:-1]

			if(splited_line[6][:-1] == "None") : 
				line_dict['direction'] = None
			else : 
				line_tab = splited_line[6][:-1][1:-1].replace("]", "").replace(",", "").split(" ")
				line_dict['direction'] = np.array([float(line_tab[0]), float(line_tab[1]), float(line_tab[2])])

			dicts_to_send.append(line_dict)
				
	return dicts_to_send

