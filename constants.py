import numpy as np

Celestial_Bodies_Dict = {
	"Sun" : {
			"name"   : "Sun",
			"mass"   : 1.9885e30,
			"mu"     : 1.32712440018e20,
			"radius" : 696342e3,
			"corps ref" : None,
			"initial_position" : [0., 0., 0.],
			"initial_velocity" : [0., 0., 0.],
			"color" : 'gold'
	 	  },

	"Mercury" : {
			"name"   : "Mercure",
			"mass"   : 3.3011e23,
			"mu"     : 2.2032e13,
			"radius" : 2439.7e3,
			"natural satellites names" : [],
			"corps ref" : "Sun",
			"initial_position" : [],
			"initial_velocity" : [],
			"color" : 'brown'
		  },

	"Venus" : {
			"name"   : "Venus",
			"mass"   : 4.8675e24,
			"mu"     : 3.24859e14,
			"radius" : 6051.8e3,
			"natural satellites names" : [],
			"corps ref" : "Sun",
			"initial_position" : [],
			"initial_velocity" : [],
			"color" : 'coral'
		  },

	"Earth" : {
			"name"   : "Earth",
			"mass"   : 5.97237e24,
			"mu"     : 3.986004418e14,
			"radius" : 6378.137e3,
			"natural satellites names" : ["Moon"],
			"corps ref" : "Sun",
			"initial_position" : [],
			"initial_velocity" : [],
			"color" : 'lightskyblue'
		 },

	"Mars" : {
			"name"   : "Mars",
			"mass"   : 6.4171e23,
			"mu"     : 4.282837e13,
			"radius" : 3389.5e3,
			"natural satellites names" : [],
			"corps ref" : "Sun",
			"initial_position" : [],
			"initial_velocity" : [],
			"color" : 'firebrick'
		 },

	"Jupiter" : {
			"name"   : "Jupiter",
			"mass"   : 1.8982e27,
			"mu"     : 1.26686534e17,
			"radius" : 69911e3,
			"natural satellites names" : [],
			"corps ref" : "Sun",
			"initial_position" : [],
			"initial_velocity" : [],
			"color" : 'orange'
		 },

	"Saturn" : {
			"name"   : "Saturn",
			"mass"   : 5.6834e26,
			"mu"     : 3.7931187e16,
			"radius" : 58232e3,
			"natural satellites names" : [],
			"corps ref" : "Sun",
			"initial_position" : [],
			"initial_velocity" : [],
			"color" : 'peachpuff'
		 },

	"Uranus" : {
			"name"   : "Uranus",
			"mass"   : 8.6810e25,
			"mu"     : 5.793939e15,
			"radius" : 25362e3,
			"natural satellites names" : [],
			"corps ref" : "Sun",
			"initial_position" : [],
			"initial_velocity" : [],
			"color" : 'mediumslateblue'
		 },

	"Neptune" : {
			"name"   : "Neptune",
			"mass"   : 1.02413e26,
			"mu"     : 6.836529e15,
			"radius" : 24622e3,
			"natural satellites names" : [],
			"corps ref" : "Sun",
			"initial_position" : [],
			"initial_velocity" : [],
			"color" : 'blue'
		 },

	"Moon" : {
			"name"   : "Moon",
			"mass"   : 7.34767309e22,
			"mu"     : 4.9048695e12,
			"radius" : 1737.4e3,
			"corps ref" : "Earth",
			"initial_position" : [],
			"initial_velocity" : [],
			"color" : 'lightgrey'
		 }
}



def EphemeridesLoader () : 
	global Celestial_Bodies_Dict

	with open("ephemerides.txt", 'r') as ephemerides_file : 

		lines = ephemerides_file.readlines()

		for line in lines :
			splited_line = line.split(',')
			del splited_line[1]
			del splited_line[-1]

			Celestial_Bodies_Dict[splited_line[0]]["initial_position"] = [1.496e11*float(elt) for elt in splited_line[1:4]]
			Celestial_Bodies_Dict[splited_line[0]]["initial_velocity"] = [1.731e6*float(elt) for elt in splited_line[4:7]]

EphemeridesLoader()

# rotationnal velocity data [rad/s]

wTe = 7.292115e-5

