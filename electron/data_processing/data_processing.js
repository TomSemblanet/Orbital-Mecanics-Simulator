function getData (raw_results, renderer_prm) {
	console.log("Simulation results ...")
	console.log(raw_results)

	if(renderer_prm["graphics"].on == true) {
		let graphics_data = parseGraphicsPrm(raw_results, renderer_prm)
		const graphics_module = require("../display/charts/graphics.js")
		graphics_module.graphicsDisplayer(graphics_data)					}

	else if (renderer_prm["ground track"].on == true) {
		let ground_track_data = getLongitudeLatitude(raw_results, renderer_prm)
		const ground_track_module = require("../display/ground_track/ground_track.js")
		ground_track_module.groundTrackDisplayer(ground_track_data)
	}
	
}


function parseGraphicsPrm (raw_results, renderer_prm) {

	/* Construit les dictionnaires {date, valeur} pour chaque paramètre orbital et chaque
			corps demandé  */ 

	var orb_param_dict = {}	

	for (const orb_param in renderer_prm.graphics.values) {
		orb_param_dict[orb_param] = []

		for (var i=0 ; i<renderer_prm.graphics.values[orb_param].length ; i++) {
			var body_unit_dict = {}
			body_unit_dict["name"] = renderer_prm.graphics.values[orb_param][i]
			body_unit_dict["vals"] = []

			for (var j=0 ; j<raw_results["time steps"].length ; j++) {
				var unit_dict = {"time": raw_results["time steps"][j], "value": raw_results[renderer_prm.graphics.values[orb_param][i]][orb_param][j]}
				body_unit_dict["vals"].push(unit_dict)
			}
			orb_param_dict[orb_param].push(body_unit_dict)
		}
	}

	return orb_param_dict
}

function getLongitudeLatitude (raw_results, renderer_prm) {

	let sat_list = renderer_prm["ground track"].sat_names
	
	var sats_dict = {}

	// Création des dictionnaire propres à chaque satellites et les listes contenant longitudes & latitudes
	for (var i=0 ; i<sat_list.length ; i++) 
		sats_dict[sat_list[i]] = []

	// Récupération des données depuis le fichier renvoyé par le moteur de calcul
	for (var j=0 ; j<sat_list.length ; j++) {
		for (var i=0 ; i<raw_results["time steps"].length ; i++) {
			sats_dict[sat_list[j]].push([raw_results[sat_list[j]].Longitude[i], raw_results[sat_list[j]].Latitude[i]])
		}
	}

	const fsLibrary  = require('fs')
	fsLibrary.writeFile('long_lat.json', JSON.stringify(sats_dict["SAT"]), (error) => { 
      
    // In case of a error throw err exception. 
    if (error)
    	console.log("ERROR "); 
	}) 

	console.log(">>>")
	console.log(sats_dict)
	return sats_dict
}

module.exports.getData = getData