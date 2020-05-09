var celestial_bodies_dict = []

function buildCelestialBodiesDict () {
	celestial_bodies_names = []

	let box_list_ = document.querySelectorAll("#celestial_bodies input")

	for(var i=0 ; i<box_list_.length ; i++) {
		if(box_list_[i].checked == true) 
			celestial_bodies_names.push(box_list_[i].name)
	}

	celestial_bodies_dict["to load"] = celestial_bodies_names
}

document.querySelector("#celestial_bodies").addEventListener("change", buildCelestialBodiesDict)

module.exports = 
{
	sendCelestialBodies : function sendCelestialBodies () {return celestial_bodies_dict}
}