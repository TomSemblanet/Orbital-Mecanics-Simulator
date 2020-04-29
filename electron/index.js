const {PythonShell} = require('python-shell')

var json_template = JSON.stringify({
			"general" : {
					"perturbations" : ["LS", "D", "SPR", "J2"]
						},


			"time" : {	
					"time step": 10,
					"starting date": "2000-01-01 12:00:00.000",
					"simulation time": 10000
						},

			"satellites": [{
					"name": "SAT1",
					"r0" : [42000000, 0, 0],
					"v0" : [0, 3078, 0],
					"mass" : 792,
					"corps_ref": "Earth"
						}],

			"maneuvers": [{
					"sat_name": "SAT1",
					"man_name": "custom acceleration",
					"value": 1000,
					"trigger_type": "date",
					"trigger_value": "2000-01-01 20:00:00.000",
					"direction": [0, 0, 0]
						}],

				"celestial bodies": {
					"to load": ["Sun", "Mercury", "Venus", "Earth", "Mars"]
						}
					})

var options = {
	mode: 'json',
	encoding: 'utf8',
	scriptPath: './engine/',
	args: [json_template]
}

PythonShell.run('main.py', options, (err, results) => {
	if(err)
		console.log(err)
})

