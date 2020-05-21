function getData (raw_results, renderer_prm) {
	console.log("Simulation results ...")
	console.log(raw_results)

	var graphics_data

	if(renderer_prm.graphics.on == true)
		graphics_data = parseGraphicsPrm(raw_results, renderer_prm)

	const graphics_module = require("../display/graphics.js")
	graphics_module.graphicsDisplayer(graphics_data)
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

module.exports.getData = getData