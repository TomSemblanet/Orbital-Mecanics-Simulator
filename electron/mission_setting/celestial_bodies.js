var celestial_bodies_names = []

function loadCelestialBodiesList () {
	celestial_bodies_names = []

	let box_list_ = document.querySelectorAll("#celestial_bodies input")

	for(var i=0 ; i<box_list_.length ; i++) {
		if(box_list_[i].checked == true) 
			celestial_bodies_names.push(box_list_[i].name)
	}

	console.log(celestial_bodies_names)
}

document.querySelector("html").addEventListener("change", loadCelestialBodiesList)

module.exports = 
{
	send_celestial_bodies : function send_celestial_bodies () {return celestial_bodies_names}
}