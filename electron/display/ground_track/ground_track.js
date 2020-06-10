// Constante à définir plus tard dans un fichier commun de constantes

const WIDTH = 1192, 
	  HEIGHT = 702,
	  LINE_WIDTH = 2,
	  TRACK_LENGTH = 650,

	  TRACK_COLORS = [`rgba(255, 0, 0, `, `rgba(146, 235, 66, `, `rgba(23, 102, 233, `, `rgba(246, 255, 43, `, `rgba(162, 16, 252, `, `rgba(194, 118, 33, `]

var COUNT = 0

var sat_data = []
	 

module.exports.groundTrackDisplayer = function (ground_track_data) {

	for (var i=0 ; i<Object.keys(ground_track_data).length ; i++) {
		sat_data.push(ground_track_data[Object.keys(ground_track_data)[i]])
	}

	adaptRawData()

	var context = document.querySelector("#ground_track_canvas").getContext('2d')

	var map = new Image ()
	map.src = '../../img/mappemonde.jpg'
	map.onload = () => {window.requestAnimationFrame( () => {draw(context, map)} )}
}

function adaptRawData () {

	for (var i=0, l=sat_data.length ; i<l ; i++) {
		for (var j=0, u=sat_data[i].length ; j<u ; j++) {

			//------------------------------------
			// Traitement des longitudes
			sat_data[i][j][0] = sat_data[i][j][0] * (180/Math.PI) // conversion degré -> radian
			sat_data[i][j][0] += 180 // décalage [-180 ; 180] -> [0 ; 360]
			sat_data[i][j][0] *= WIDTH/360 // extention [0 ; 360] -> [0 ; WIDTH]

			//------------------------------------
			// Traitement des latitudes
			sat_data[i][j][1] = sat_data[i][j][1] * (180/Math.PI) // conversion degré -> radian
			sat_data[i][j][1] += 90 // décalage [-90 ; 90] -> [0 ; 180]
			sat_data[i][j][1] *= HEIGHT/180 // extention [0 ; 180] -> [0 ; HEIGHT]
			sat_data[i][j][1] = HEIGHT - sat_data[i][j][1] // renversement [0 ; HEIGHT] -> [HEIGHT ; 0] puisque les pixels sont croissants vers le bas
		}
	}
}

function draw (context, map) {

	context.clearRect(0, 0, WIDTH, HEIGHT)
	context.drawImage(map, 0, 0, WIDTH, HEIGHT)
	context.lineWidth = LINE_WIDTH; 

	const paths=[], lines=[]

	// --------------------------------------------
	//  Création des paths

	for (var i=0, l=sat_data.length ; i<l ; i++) {
		paths.push(d3.geoPath().context(context));
	}

	// --------------------------------------------
	//  Création des lines
	if(COUNT < TRACK_LENGTH)
		for (var i=0, l=sat_data.length ; i<l ; i++) {
			lines.push(sat_data[i].slice(0, COUNT))
		}

	else 
		for (var i=0, l=sat_data.length ; i<l ; i++) {
			lines.push(sat_data[i].slice(COUNT-TRACK_LENGTH, COUNT))
		}

	let opacity = 0;
	let decay = 1/lines[0].length;

	while(lines[0].length > 1) {

		for (var i=0, l=sat_data.length ; i<l ; i++) {

			let start = lines[i][0],
		        end = lines[i][1];

		   	context.strokeStyle = TRACK_COLORS[i] + `${opacity})`;

		    if(Math.abs(end[0] - start[0]) < 200 && Math.abs(end[1] - start[1]) < 200) {
				context.beginPath()
				paths[i]( {type: 'LineString',  coordinates: [start, end],} )
				context.stroke() 	
			}

			lines[i].shift();
		}

		opacity += decay;
	}

	COUNT = (COUNT + 1) % (sat_data[0].length)

	window.requestAnimationFrame( () => {draw(context, map)} )
}





