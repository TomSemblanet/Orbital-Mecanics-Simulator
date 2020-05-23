module.exports = 
{
	sendPythonShell : function sendPythonShell (dict_to_send) {
		const {PythonShell} = require('python-shell')

		var file_ = JSON.stringify(dict_to_send)

		var options = {
			mode: "json",
			encoding: "utf8",
			scriptPath: "./engine/",
			args: [file_]
		}

		console.log(dict_to_send)

		PythonShell.run('main.py', options, (err, simulation_results) => {
			if(err) 
				console.log(err)
			else {
				let data_processing = require("./data_processing.js")
				console.log(":(")
				data_processing.getData(simulation_results[0], dict_to_send.exploitation)
				console.log(":)")
			}
		})
	}
}