# This file loads all the parameters both of the simulation and of the bodies (satellites and celestial bodies)
# It simply reads the parameters text file stored in DATA_FILE and extract from it all the parameters.

import numpy as np

import constants as cst

DATA_FILE = "./scenarios/DATA.txt"

def parametersLoader () : 
	
	""" 
	Calls all specific functions which will load simulation parameters from the text file
		specified in DATA_FILE 
	"""

	with open(DATA_FILE, 'r') as data_file : 

		lines = data_file.readlines()

		for catgr in parameters.keys() : 
			for indic, line in enumerate(lines) : 
				if(catgr.upper() in line) : 
					begin_indice = indic+2
					end_indice = begin_indice
					while(not('=' in lines[end_indice])) : end_indice += 1
					end_indice -= 2
					parameters[catgr]["loader func"](lines[begin_indice:end_indice])



# def generalParametersLoader (lines) : 
	
# 	parameters['general']['Keplerian simulation'] = (lines[0].split('[')[1][0] == 'v')


def generalParametersLoader (generals_prm) : 

	parameters['general']["perturbations"] = generals_prm["perturbations"]

	parameters["time"]["general time step"] = generals_prm["time step"]
	parameters["time"]["time step"] = parameters["time"]["general time step"]

	parameters["time"]["starting date"] = generals_prm["starting date"]
	parameters["time"]["initial julian date"] = 367*int(parameters["time"]["starting date"][0:4]) - int((7*(int(parameters["time"]["starting date"][0:4])+int((int(parameters["time"]["starting date"][5:7])+9)/12)))/4) \
					+ int(275*int(parameters["time"]["starting date"][5:7])/9) + int(parameters["time"]["starting date"][8:10]) + 1721013.5 + (((int(parameters["time"]["starting date"][17:19])/60) \
					+ int(parameters["time"]["starting date"][14:16]))/60+int(parameters["time"]["starting date"][11:13]))/24 - 2451545


	parameters["time"]["simulation time"] = generals_prm["simulation time"]
	parameters["time"]["elapsed time"] = 0

# def timeParametersLoader (time_prm) :

# 	parameters["time"]["general time step"] = time_prm["time step"]
# 	parameters["time"]["time step"] = parameters["time"]["general time step"]

# 	parameters["time"]["starting date"] = time_prm["starting date"]
# 	parameters["time"]["initial julian date"] = 367*int(parameters["time"]["starting date"][0:4]) - int((7*(int(parameters["time"]["starting date"][0:4])+int((int(parameters["time"]["starting date"][5:7])+9)/12)))/4) \
# 					+ int(275*int(parameters["time"]["starting date"][5:7])/9) + int(parameters["time"]["starting date"][8:10]) + 1721013.5 + (((int(parameters["time"]["starting date"][17:19])/60) \
# 					+ int(parameters["time"]["starting date"][14:16]))/60+int(parameters["time"]["starting date"][11:13]))/24 - 2451545


# 	parameters["time"]["simulation time"] = time_prm["simulation time"]
# 	parameters["time"]["elapsed time"] = 0

# def timeParametersLoader (lines) :  

# 	""" 
# 	Loads the parameters related to the passage of time to know : 
# 				- The general time step : the time step at which the simulation must return after an adaption 
# 					of the real-time time step (adaption due to a maneuver - for example)
# 				- The time step : the real-time time step of the simulation, which can be modified to reach 
# 					a particular epoch 
# 				- Starting date : the starting date of the simulation under the form YEAR-MONTH-DAY HOUR:MINUTE:SECOND.MILLISECOND
# 				- Initial Julian date : the starting Julian date 

# 		Input : interesting lines for loading parameters

# 		Return : None 
# 	"""

# 	parameters["time"]["general time step"] = int(lines[1].split('~')[1])
# 	parameters["time"]["time step"] = parameters["time"]["general time step"]

# 	parameters["time"]["starting date"] = lines[0].split('~')[1].lstrip()[:-1]
# 	parameters["time"]["initial julian date"] = 367*int(parameters["time"]["starting date"][0:4]) - int((7*(int(parameters["time"]["starting date"][0:4])+int((int(parameters["time"]["starting date"][5:7])+9)/12)))/4) \
# 					+ int(275*int(parameters["time"]["starting date"][5:7])/9) + int(parameters["time"]["starting date"][8:10]) + 1721013.5 + (((int(parameters["time"]["starting date"][17:19])/60) \
# 					+ int(parameters["time"]["starting date"][14:16]))/60+int(parameters["time"]["starting date"][11:13]))/24 - 2451545
# 	parameters["time"]["simulation time"] = float(lines[2].split('~')[1].lstrip()[:-1])
	
# 	parameters["time"]["elapsed time"] = 0


def applicationsParametersLoader (lines) : 

	""" 
	Loads the parameters related to the simulation in general to know : 
				- The simulation speed : will adapt refresh rate of the plot
				- Applications on : determine the applications to run (Spatial View / Ground Track / Parameters Plot)
					they all can be runned independantly
				- Show bodies data : if On, orbital parameters of specified bodies will be displayed (slow down the simulation)
				- Bodies data displayed : list of the bodies whose orbital parameters are displayed if the previous parameter is On 
	
	Input : interesting lines for loading parameters

	Return : None 

	"""

	for x in lines[1].split(':')[1].split(']')[:-1] :
		if(x[-1] == 'v') : 
			parameters["applications"]["simulation speed"] = x.lstrip().replace("[v", '')[:-1]

	parameters["applications"]["calculation repeat"] = parameters["applications"]["simulation speed dict"][parameters["applications"]["simulation speed"]]
	
	for x in lines[0].split(':')[1].split(']')[:-1] : 
		if(x[-1] == 'v') : 
			parameters["applications"]["applications on"].append(x.lstrip().replace(" [v", ""))

	parameters["applications"]["leader application"] = parameters["applications"]["applications on"][0]

	if(lines[2].split(':')[1].lstrip()[:-1].split(' ')[0].replace('[', '').replace(']', '') == 'v') : parameters["applications"]["show bodies data"] = True
	else : parameters["applications"]["show bodies data"] = False

	for sat_name in lines[3].split(':')[1].lstrip()[:-1].split(' ') :
		parameters["applications"]["bodies data displayed"].append(sat_name)


def spatialViewParametersLoader (lines) : 

	""" 
	Loads the parameters related to the Spatial View application to know : 
				- Display mode : if on "trajectory prediction" the orbit of each satellite will be displayed, if not, 
						only their trajectories will be displayed
				- Following mode : if on, the window will follow the body on which the focus is placed 
				- Body to follow : name of the body (either satellite or celestial body) on which the focus is placed
				- Window radius : radius (in meter) of the view around the body on which the focus is placed 

	Input : interesting lines for loading parameters

	Return : None 
	
	"""	

	for x in lines[0].split(':')[1].split(']')[:-1] : 
		if (x[-1] == 'v') : 
			parameters["spatial view"]["display mode"] = x.lstrip().replace(' [v', '')

		if (lines[1].split('[')[1][0] == 'v') : 
			parameters["spatial view"]["following mode"] = True
			parameters["spatial view"]["body to follow"] = lines[1].split('[')[1].split("--")[1].replace('\n', '').split(' ')[0]
			parameters["spatial view"]["window radius"] = float(lines[1].split('[')[1].split("--")[1].replace('\n', '').split(' ')[1])



def groundTrackParametersLoader (lines) : 
	""" 
	No parameters for the Ground Track application for the moment 
	"""
	pass

def parametersPlotParametersLoader (lines) :

	""" 
	Loads the parameters related to the Spatial View application to know : 
				- Parameter to plot : name of the parameter whose evolution is plotted
				- Sattelites displayer : name of the satellite whose parameter is plotted
				- Historic length : length (in second) of the historic of the plotted parameters 

	Input : interesting lines for loading parameters

	Return : None 
	
	"""

	parameters["parameters plot"]["parameter to plot"] = lines[0].split(':')[1][:-1].lstrip()
	parameters["parameters plot"]["satellites displayed"] = lines[1].split(':')[1].lstrip()[:-1].split(' ')
	parameters["parameters plot"]["historic length"] = float(lines[2].split(':')[1])


def celestialBodiesLoader () : 

	""" 
	Loads the celestial bodies specified in the parameters text file - section "Celestial bodies"

	Input : None

	Return : the list of the names the celestial bodies which will be simulated 

	"""

	celestial_bodies_to_load = [] 

	with open(DATA_FILE, 'r') as data_file : 

		begin_indice, end_indice = 0, 0
		lines = data_file.readlines()

		for indic, line in enumerate(lines) : 
			if("celestial bodies".upper() in line) : 
				begin_indice = indic+2
		
		for l in lines[begin_indice].replace('-', '').replace('\n', '').split(']')[:-1] : 

			if(l[-1] == 'v') : 
				if(len([body_name for body_name in celestial_bodies_to_load if (cst.Celestial_Bodies_Dict[body_name]['central'] == True)]) == 0) : 
					cst.Celestial_Bodies_Dict[l.lstrip().replace(' [v', '')]['central'] = True
				celestial_bodies_to_load.append(l.lstrip().replace(' [v', ''))

	return celestial_bodies_to_load


def satellitesLoader () : 

	""" 
	Loads the satellites and their parameters specified in the parameter text file - section "Satellites" - to know :
				- The name : simply the name of the satellite
				- The initial position : r0 is the initial position of the satellite in the referential of the body
							around which it orbits initially
				- The initial velocity : v0 is the initial velocity of the satellite in the referential of the body
							around which it orbits initially
				- The referent body : it is the body around which the body orbits initially
				- The color : simply the color of the satellite plot 

	Input : None

	Return : a list containing dictionnaries describing each the required parameters to load a satellite

	"""

	dicts_to_send = []

	with open(DATA_FILE, 'r') as data_file : 

		begin_indice, end_indice = 0, 0
		lines = data_file.readlines()

		for indic, line in enumerate(lines) : 
			if("satellites".upper() in line) : 
				begin_indice = indic+2
			if("maneuvers".upper() in line) : 
				end_indice = indic-2

		for line in lines[begin_indice:end_indice] : 
			splited_line = line.split('--')
			line_dict = dict()

			line_dict['name'] = splited_line[1].lstrip().replace(" ", "")

			string_tab = splited_line[2][1:-2]
			line_dict['r0'] = np.array([float(string_tab.split(',')[0].lstrip()), float(string_tab.split(',')[1].lstrip()), float(string_tab.split(',')[2].lstrip())])
	
			string_tab = splited_line[3][1:-2]
			line_dict['v0'] = np.array([float(string_tab.split(',')[0].lstrip()), float(string_tab.split(',')[1].lstrip()), float(string_tab.split(',')[2].lstrip())])
			
			line_dict['mass'] = float(splited_line[4].replace(" ", ""))

			line_dict['corps_ref'] = splited_line[5].replace(" ", "")

			line_dict['color'] = splited_line[6].replace("\n", "")

			dicts_to_send.append(line_dict)

	return dicts_to_send


def maneuverLoader () : 

	"""
	Loads the satellites maneuvers and their parameters specified in the parameter text file - section "Maneuvers" - to know :
				- The satellite name : the name of the satellite to which the maneuver will be applied
				- The maneuver name : the name of the maneuver
				- The value of the maneuver : the meaning of this parameters depends on the maneuver name, for example, for a
						modification of the apogee the value est the algebrical value of the modification (in meter), for a 
						modification of the inclinaison the value is the algebrical value of the modification (in degree), 
						for a custom acceleration the value is the algebrical deltaV (in meter per seconds) etc ...
				- The trigger type : the trigger type is the way the maneuver will be triggered, it can be either a given time
						or a given true anomaly on its orbit
				- The trigger value : the trigger value depends on the trigger type, it is either a given date or a true anomaly
				- The direction : it's the direction in which the propulsion has to be done. A [0, 0, 0] direction just means the 
						propulsion has to be done in the direction of the velocity 


	Input : None

	Return : a list containing dictionnaries describing each the required parameters to load a maneuver

	"""

	dicts_to_send = []

	with open(DATA_FILE, 'r') as data_file : 

		begin_indice, end_indice = 0, 0
		lines = data_file.readlines()

		for indic, line in enumerate(lines) : 
			if("maneuvers".upper() in line) : 
				begin_indice = indic+2
			if("time".upper() in line) : 
				end_indice = indic-2

		for line in lines[begin_indice:end_indice] : 
			splited_line = line.split('--')
			line_dict = dict()

			line_dict['sat_name'] = splited_line[1][:-1]

			line_dict['man_name'] = splited_line[2][:-1]

			if(line_dict['man_name'] == "orbital rendez-vous") : 
				line_dict["value"] = dict()
				split = splited_line[3][:-1].replace("[", "").replace("]", "").replace(",", "").split(" ")

				line_dict["value"]["position_to_reach"] = np.array([float(split[0]), float(split[1]), float(split[2])])
				line_dict["value"]["date"] = split[3]+" "+split[4]
			else : 
				line_dict['value'] = float(splited_line[3][:-1])

			line_dict['trigger_type'] = splited_line[4][:-1]

			try :
				line_dict['trigger_value'] = float(splited_line[5][:-1])
			except : 
				line_dict['trigger_value'] = splited_line[5][:-1]

			line_dict['direction'] = splited_line[6][:-1]

			if(splited_line[6][:-1] == "None") : 
				line_dict['direction'] = None
			else : 
				line_tab = splited_line[6][:-1][1:-1].replace("]", "").replace(",", "").split(" ")
				line_dict['direction'] = np.array([float(line_tab[0]), float(line_tab[1]), float(line_tab[2])])

			dicts_to_send.append(line_dict)
				
	return dicts_to_send



parameters = {
	"general" : {
		"perturbations" : list()
	},

	"time" : 
	{
		"general time step" : int(),
		"time step" : int(),
		"starting date" : str(),
		"current date" : str(),
		"initial julian date" : float(), # [days]  ~ following J2000
		"current julian date" : float(), # [days]
		"simulation time" : float(),
		"elapsed time" : float() # [sec]
	}
}


