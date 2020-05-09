let open_creator_button_ = document.querySelector("#maneuvers_invite"),
	confirm_maneuver_button = document.querySelector(".confirm_maneuver"),
	maneuvers_frame_ = document.querySelector("#maneuvers_frame"),
	displayer_frame = document.querySelector("#maneuvers_invite"),
	creator_frame = document.querySelector("#maneuvers_creator")

open_creator_button_.addEventListener("click", openCreator)
confirm_maneuver_button.addEventListener("click", closeCreator)
maneuvers_frame_.addEventListener("change", LambertProblemParameters)

function openCreator () {
	maneuvers_frame_.classList.replace("invite", "creation")
	displayer_frame.style.display = "none";
	creator_frame.style.display = "block";
}

function closeCreator () {
	maneuvers_frame_.classList.replace("creation", "invite")
	displayer_frame.style.display = "block";
	creator_frame.style.display = "none";
}

function LambertProblemParameters () {
	if(document.querySelector("#first_line #maneuvers_panel").value == "rdv") {
		document.querySelector("#classic_third_line").style.display = "none"
		document.querySelector("#Lambert_third_line").style.display = "block"
	}

	else {
		document.querySelector("#classic_third_line").style.display = "block"
		document.querySelector("#Lambert_third_line").style.display = "none"
	}
}


let sat_list = [], sat_dict = {},
	man_list = [], man_dict = {}


function addManeuver () {

	// Ajout de tout les champs HTML au dictionnaire man_dict


	let type_ = document.querySelector("#first_line #maneuvers_panel"),
		name_ = document.querySelector("#maneuver_name"),
		trigger_type_ = document.querySelector("#second_line #maneuver_trigger "),
		trigger_value_ = document.querySelector("#second_line #trigger_value"),
		arvl_date_, x_arvl_, y_arvl_, z_arvl_, value_
		
	if(type_.value == "rdv") {
		arvl_date_ = document.querySelector("#Lambert_third_line #arvl_date")
		x_arvl_ = document.querySelector("#Lambert_third_line #x_rdv")
		y_arvl_ = document.querySelector("#Lambert_third_line #y_rdv")
		z_arvl_ = document.querySelector("#Lambert_third_line #z_rdv")

		// console.log(x_arvl_.value)
	}

	else 
		value_ = document.querySelector("#classic_third_line #maneuver_value")

	let x_dir_ = document.querySelector("#fourth_line #x_dir"),
		y_dir_ = document.querySelector("#fourth_line #y_dir"),
		z_dir_ = document.querySelector("#fourth_line #z_dir")

	man_dict["man name"] = type_.value
	man_dict["name"] = name_.value 
	man_dict["trigger type"] = trigger_type_.value
	man_dict["trigger value"] = trigger_value_.value
	if(type_.value == "rdv") 
		man_dict["value"] = [arvl_date_.value, [x_arvl_.value, y_arvl_.value, z_arvl_.value]]
	else
		man_dict["value"] = value_.value
	man_dict["direction"] = [x_dir_.value, y_dir_.value, z_dir_.value]

	// Réinitialisation des champs HTML

	if(type_.value == "rdv") {
		arvl_date_.value = null
		x_arvl_.value = null
		y_arvl_.value = null
		z_arvl_.value = null
	}

	else 
		value_.value = null

	type_.value = "custom"
	name_.value = null
	trigger_type_.value = "date"
	trigger_value_.value = null

	x_dir_.value = null
	y_dir_.value = null
	z_dir_.value = null

	// Ajout du dictionnaire man_dict à la liste man_list

	man_list.push(man_dict)

	// Réinitialisation du dictionnaire man_dict

	man_dict = {}

	// Passage en mode invite

	displayer_frame.style.display = "block"
	creator_frame.style.display = "none"
	maneuvers_frame_.classList.replace("creation", "invite")

}

function addSatellite () {

	// Ajout de tout les champs HTML au dictionnaire sat_dict

	let name_ = document.querySelector("#sat_name"),
		mass_ = document.querySelector("#mass"),
		ref_body_ = document.querySelector("#ref_body"),
		surface_ = document.querySelector("#surface"),
		xi_ = document.querySelector("#xi"),
		yi_ = document.querySelector("#yi"),
		zi_ = document.querySelector("#zi"),
		vxi_ = document.querySelector("#vxi"),
		vyi_ = document.querySelector("#vyi"),
		vzi_ = document.querySelector("#vzi")

	sat_dict["name"] = name_.value
	sat_dict["mass"] = mass_.value
	sat_dict["corps ref"] = ref_body_.value 
	sat_dict["surface"] = surface_.value 
	sat_dict["r0"] = [xi_.value, yi_.value, zi_.value]
	sat_dict["v0"] = [vxi_.value, vyi_.value, vzi_.value]

	// Réinitialisation des champs HTML

	name_.value = null 
	mass_.value = null 
	ref_body_.value = null 
	surface_.value = null 
	xi_.value = null 
	yi_.value = null 
	zi_.value = null 
	vxi_.value = null 
	vyi_.value = null 
	vzi_.value = null 

	// Ajout de la liste man_list au dictionnaire sat_dict 

	sat_dict["maneuvers"] = (man_list)

	// Ajout du dictionnaire sat_dict à la liste sat_list

	sat_list.push(sat_dict)

	// Ajout d'un satellite dans la liste HTML

	var sat_name_parag = document.createElement("p")
	sat_name_parag.classList.add("txt")
	sat_name_parag.style.fontSize = "1.5em"
	sat_name_parag.innerHTML = sat_dict["name"]
	sat_name_parag.style.marginTop = "10px"
	sat_name_parag.style.marginBottom = "5px" 

	var inner_div_list = []

	for (var i=0 ; i<man_list.length ; i++) {

		var inner_div = document.createElement("div")
		inner_div.style.display = "flex"
		inner_div.style.marginLeft = "60px"

		let man_name_parag = document.createElement("p")
		man_name_parag.classList.add("txt")
		man_name_parag.style.fontSize = "0.8em"
		man_name_parag.innerHTML = man_list[i]["name"]

		man_name_parag.style.marginTop = "0px"
		man_name_parag.style.marginBottom = "0px" 

		inner_div.appendChild(man_name_parag)

		inner_div_list.push(inner_div)
	}

	var global_div = document.createElement("div")
	global_div.style.marginBottom = "10px"
	global_div.appendChild(sat_name_parag)
	for(var i=0 ; i < inner_div_list.length ; i++) {
		global_div.appendChild(inner_div_list[i])
	}

	document.querySelector("#satellites_live_displayer").appendChild(global_div)

	// Réinitialisation du dictionnaire sat_dict 

	sat_dict = {}

	// Réinitialisation de la liste man_list

	man_list = []
}

document.querySelector(".confirm_maneuver").addEventListener("click", addManeuver)
document.querySelector(".add_satellite").addEventListener("click", addSatellite)


module.exports = 
{
	sendSatellites : function sendSatellites () {return sat_list},

	send_satellites_names : function send_satellites_names () {
		let names = []
		for(var i=0 ; i<sat_list.length ; i++) {
			names.push(sat_list[i]["name"])
		}
		return names
	}
}