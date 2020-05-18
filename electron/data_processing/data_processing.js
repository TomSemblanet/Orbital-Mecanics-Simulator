var results_ = {}

function getData (simulation_results, renderer_prm) {
	console.log("Simulation results ...")
	console.log(simulation_results)

	results_ = simulation_results

	if(renderer_prm.graphics.on == true)
		parseGraphicsPrm(simulation_results, renderer_prm)
}


function parseGraphicsPrm (simulation_results, renderer_prm) {

}

module.exports.getData = getData