module.exports = {
	missionLoader : function missionLoader (file_name) {

		const json_file = require('../historic/' + file_name + '.json')
		const generals = require("./generals.js"),
			  satellites = require("./satellites.js"),
			  celestial_bodies = require("./celestial_bodies.js"),
			  exploitation = require("./exploitation.js")

		// General parameters loader
		generals.loadGeneralsFromFile(json_file)

		// Celestial bodies loader
		celestial_bodies.loadCelestialBodiesFromFile(json_file)

		// Satellites loader
		for (var i=0 ; i<json_file["satellites"].length ; i++) { satellites.addSatelliteFromFile(json_file["satellites"][i]) }

		// Exploitation loader
		
	}
}