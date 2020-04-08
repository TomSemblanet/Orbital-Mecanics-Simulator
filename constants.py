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
			"color" : 'gold',

			"central" : bool() 
	 	  },

	"Mercury" : {
			"name"   : "Mercure",
			"mass"   : 3.3011e23,
			"mu"     : 2.2032e13,
			"radius" : 2439.7e3,
			"oblateness" : 0.000,
			"J2" : 6.0e-5,
			"natural satellites names" : [],
			"corps ref" : "Sun",
			"initial_position" : [],
			"initial_velocity" : [],
			"color" : 'brown',

			"central" : bool()
		  },

	"Venus" : {
			"name"   : "Venus",
			"mass"   : 4.8675e24,
			"mu"     : 3.24859e14,
			"radius" : 6051.8e3,
			"oblateness" : 0.000,
			"J2" : 2.7e-5,
			"natural satellites names" : [],
			"corps ref" : "Sun",
			"initial_position" : [],
			"initial_velocity" : [],
			"color" : 'coral',

			"central" : bool()
		  },

	"Earth" : {
			"name"   : "Earth",
			"mass"   : 5.97237e24,
			"mu"     : 3.986004418e14,
			"radius" : 6378.137e3,
			"oblateness" : 0.003353,
			"J2" : 1.1e-3,
			"natural satellites names" : ["Moon"],
			"corps ref" : "Sun",
			"initial_position" : [],
			"initial_velocity" : [],
			"color" : 'lightskyblue',

			"central" : bool()
		 },

	"Mars" : {
			"name"   : "Mars",
			"mass"   : 6.4171e23,
			"mu"     : 4.282837e13,
			"radius" : 3389.5e3,
			"oblateness" : 0.00648,
			"J2" : 2.0e-3,
			"natural satellites names" : [],
			"corps ref" : "Sun",
			"initial_position" : [],
			"initial_velocity" : [],
			"color" : 'firebrick',

			"central" : bool()
		 },

	"Jupiter" : {
			"name"   : "Jupiter",
			"mass"   : 1.8982e27,
			"mu"     : 1.26686534e17,
			"radius" : 69911e3,
			"oblateness" : 0.06487,
			"J2" : 1.5e-2,
			"natural satellites names" : [],
			"corps ref" : "Sun",
			"initial_position" : [],
			"initial_velocity" : [],
			"color" : 'orange',

			"central" : bool()
		 },

	"Saturn" : {
			"name"   : "Saturn",
			"mass"   : 5.6834e26,
			"mu"     : 3.7931187e16,
			"radius" : 58232e3,
			"oblateness" : 0.09796,
			"J2" : 1.6e-2,
			"natural satellites names" : [],
			"corps ref" : "Sun",
			"initial_position" : [],
			"initial_velocity" : [],
			"color" : 'peachpuff',

			"central" : bool()
		 },

	"Uranus" : {
			"name"   : "Uranus",
			"mass"   : 8.6810e25,
			"mu"     : 5.793939e15,
			"radius" : 25362e3,
			"oblateness" : 0.02293,
			"J2" : 1.2e-2,
			"natural satellites names" : [],
			"corps ref" : "Sun",
			"initial_position" : [],
			"initial_velocity" : [],
			"color" : 'mediumslateblue',

			"central" : bool()
		 },

	"Neptune" : {
			"name"   : "Neptune",
			"mass"   : 1.02413e26,
			"mu"     : 6.836529e15,
			"radius" : 24622e3,
			"oblateness" : 0.01708,
			"J2" : 4.0e-3,
			"natural satellites names" : [],
			"corps ref" : "Sun",
			"initial_position" : [],
			"initial_velocity" : [],
			"color" : 'blue',

			"central" : bool()
		 },

	"Moon" : {
			"name"   : "Moon",
			"mass"   : 7.34767309e22,
			"mu"     : 4.9048695e12,
			"radius" : 1737.4e3,
			"corps ref" : "Earth",
			"initial_position" : [],
			"initial_velocity" : [],
			"color" : 'lightgrey',

			"central" : bool()
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

			Celestial_Bodies_Dict[splited_line[0]]["initial_position"] = np.array([1.496e11*float(elt) for elt in splited_line[1:4]])
			Celestial_Bodies_Dict[splited_line[0]]["initial_velocity"] = np.array([1.731e6*float(elt) for elt in splited_line[4:7]])

EphemeridesLoader()

# rotationnal velocity data [rad/s]

wTe = 7.292115e-5

