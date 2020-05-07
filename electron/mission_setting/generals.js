var btn1 = document.querySelector(".maneuvers_invite"),
	btn2 = document.querySelector(".confirm_maneuver"),
	frame = document.querySelector(".maneuvers_frame"),
	displayer_ = document.querySelector(".maneuvers_invite")
	creator_ = document.querySelector(".maneuvers_creator")

	man_frame = document.querySelector(".maneuvers_frame")

function func ()  {
	if(frame.classList.contains("creation")) 
		frame.classList.replace("creation", "invite")
	
	else {
		frame.classList.replace("invite", "creation")
	}

	if(displayer_.style.display == "none") {
		displayer_.style.display = "block";
		creator_.style.display = "none";
	}

	else {
		displayer_.style.display = "none";
		creator_.style.display = "block";
	}
}

btn1.addEventListener("click", func)
btn2.addEventListener("click", func)

man_frame.addEventListener("change", ()=>{
	if(document.querySelector("#first_line #maneuvers_panel").value == "rdv") {
		document.querySelector("#classic_third_line").style.display = "none"
		document.querySelector("#Lambert_third_line").style.display = "block"
	}

	else {
		document.querySelector("#classic_third_line").style.display = "block"
		document.querySelector("#Lambert_third_line").style.display = "none"
	}
})

