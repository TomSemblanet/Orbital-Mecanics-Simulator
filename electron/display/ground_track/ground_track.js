var ground_track = []

const N = 5000,
	  w = 0.05	

for (var i=0 ; i<N ; i++) {
	var longitude = ((-180 + 360*(N-i)/N) + 180) * 900/360,
		latitude = 450 - (Math.cos(w * longitude) + 1) * 450/2

	ground_track.push([longitude, latitude])
	console.log(ground_track[i])
}

const canvas = document.querySelector("#ground_track_canvas"),
	  context = canvas.getContext('2d')

let img_ = new Image ()
img_.src = "../../img/mappemonde.jpg"
img_.onload = () => {
	context.drawImage(img_, 0, 0, 900, 900/2)
	drawPath()  }


function drawPath () {
	const path = d3.geoPath()
    		       .context(context);

	let line = ground_track.slice();
	const lineWidth = 1.5

	context.lineWidth = lineWidth; 

	let opacity = 1.0;
	let decay = opacity / line.length;

	while (line.length > 1) {
		let start = line[0],
		    end = line[1];
		      
		context.strokeStyle = `rgba(255, 0, 0, ${opacity})`;

		let segment = {
		  type: 'LineString',
		  coordinates: [start, end],
		};

		context.beginPath()
		path(segment)
		context.stroke()

		opacity -= decay;
	    line.shift();
	}
}





