var header_buttons = document.querySelectorAll(".frame"),
	prm_windows = document.querySelectorAll(".prm_window")

var curr_frame_ind = 0 

function setCurrentFrame () {
	for(var i=0 ; i<4 ; i++) {
		if(i == curr_frame_ind && (prm_windows[i].style.display == "none")) {
			prm_windows[i].style.display = "block"
		}
		else if (i != curr_frame_ind && prm_windows[i].style.display == "block") {
			prm_windows[i].style.display= "none"
		}
	}
}


header_buttons[0].addEventListener("click", () => {
	curr_frame_ind = 0
	setCurrentFrame()
})
header_buttons[1].addEventListener("click", () => {
	curr_frame_ind = 1
	setCurrentFrame()
})
header_buttons[2].addEventListener("click", () => {
	curr_frame_ind = 2
	setCurrentFrame()
})
header_buttons[3].addEventListener("click", () => {
	curr_frame_ind = 3
	setCurrentFrame()
})
header_buttons[3].addEventListener("click", () => {
	curr_frame_ind = 3
	setCurrentFrame()
})



// Reception des dictionnaires et / ou listes

var generals = require("./generals.js"),
	satellites = require("./satellites.js"),
	celestial_bodies = require("./celestial_bodies.js")

var generals_prm_getter = generals.send_generals_prm(),
	satellites_getter = satellites.send_satellites(),
	celestial_bodies_getter = celestial_bodies.send_celestial_bodies()



