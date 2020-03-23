import numpy as np

DATA_FILE = "Scenarios/DATA_example1.txt"

def parametersLoader () : 
	
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


def timeParametersLoader (lines) :  

	parameters["time"]["general time step"] = int(lines[1].split('~')[1])
	parameters["time"]["time step"] = parameters["time"]["general time step"]
	parameters["time"]["starting date"] = lines[0].split('~')[1].lstrip()[:-1]
	parameters["time"]["initial julian date"] = 367*int(parameters["time"]["starting date"][0:4]) - int((7*(int(parameters["time"]["starting date"][0:4])+int((int(parameters["time"]["starting date"][5:7])+9)/12)))/4) \
					+ int(275*int(parameters["time"]["starting date"][5:7])/9) + int(parameters["time"]["starting date"][8:10]) + 1721013.5 + (((int(parameters["time"]["starting date"][17:19])/60) \
					+ int(parameters["time"]["starting date"][14:16]))/60+int(parameters["time"]["starting date"][11:13]))/24 - 2451545
	parameters["time"]["elapsed time"] = 0


def applicationsParametersLoader (lines) : 

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
	
	for x in lines[0].split(':')[1].split(']')[:-1] : 
		if(x[-1] == 'v') : 
			parameters["spatial view"]["display mode"] = x.lstrip().replace(' [v', '')

	parameters["spatial view"]["following mode"] = (lines[1].split('[')[1][0] == 'v') 


def groundTrackParametersLoader (lines) : 
	pass

def parametersPlotParametersLoader (lines) :

	parameters["parameters plot"]["parameter to plot"] = lines[0].split(':')[1][:-1].lstrip()
	parameters["parameters plot"]["satellites displayed"] = lines[1].split(':')[1].lstrip()[:-1].split(' ')
	parameters["parameters plot"]["historic length"] = float(lines[2].split(':')[1])


def celestialBodiesLoader () : 

	celestial_bodies_to_load = [] 

	with open(DATA_FILE, 'r') as data_file : 

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

	with open(DATA_FILE, 'r') as data_file : 

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

	with open(DATA_FILE, 'r') as data_file : 

		begin_indice, end_indice = 0, 0
		lines = data_file.readlines()

		while (lines[begin_indice] != "=========    MANEUVERS    =========\n") : begin_indice+=1
		begin_indice+=2
		end_indice=begin_indice

		while (lines[end_indice] != "=========      TIME      =========\n") :	end_indice+=1
		end_indice-=2

		for line in lines[begin_indice:end_indice] : 
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
	"time" : 
	{
		"loader func" : timeParametersLoader,
		"general time step" : int(),
		"time step" : int(),
		"starting date" : str(),
		"current date" : str(),
		"initial julian date" : int(), # [days]  ~ following J2000
		"current julian date" : int(), # [days]

		"elapsed time" : int() # [sec]
	},

	"applications" : 
	{
		"loader func" : applicationsParametersLoader,
		"simulation speed dict" : {"slow" : 1, 
								   "medium" : 2,
								   "high" : 3,
								   "very high" : 4},
		"simulation speed" : str(),
		"calculation repeat" : int(),
		"applications on" : list(),
		"leader application" : int(),
		"show bodies data" : bool(),
		"bodies data displayed" : list()
	},

	"spatial view" : 
	{
		"loader func" : spatialViewParametersLoader,
		"display mode" : str(),
		"following mode" : bool()
	},

	"ground track" : 
	{
		"loader func" : groundTrackParametersLoader,
	},

	"parameters plot" : 
	{
		"loader func" : parametersPlotParametersLoader,
		"parameter to plot" : str(),
		"satellites displayed" : list(),
		"historic length" : int()
	},
}
