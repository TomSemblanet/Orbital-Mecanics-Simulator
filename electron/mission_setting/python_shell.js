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

		PythonShell.run('main.py', options, (err, results) => {
			if(err) 
				console.log(err)
			else 
				console.log(results)
		})
	}
}