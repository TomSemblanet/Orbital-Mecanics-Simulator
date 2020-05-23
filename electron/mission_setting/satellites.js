const exploitation = require("./exploitation.js")


let open_creator_button_ = document.querySelector("#maneuvers_invite") // Cadre contenant le bouton "Ajouter une manoeuvre"
open_creator_button_.addEventListener("click", openCreator) // [LISTENER] Création du listener appelant la fonction openCreator à chaque clique sur la fenêtre

let creator_frame = document.querySelector("#maneuvers_creator") // Cadre général de paramétrage d'une nouvelle manoeuvre

let confirm_maneuver_button = document.querySelector(".confirm_maneuver") // '+' permettant de valider un paramétrage de manoeuvre
confirm_maneuver_button.addEventListener("click", addManeuver) // [LISTENER] Création du listener appelant la fonction closeCreator à chaque clique sur le bouton de validation

let confirm_sat_button = document.querySelector(".add_satellite") // '+' permettant de valider la création d'un satellite
confirm_sat_button.addEventListener("click", addSatellite) // [LISTENER] Création du listener appelant la fonction addSatellite à chaque clique sur le bouton de validation

let maneuvers_frame_ = document.querySelector("#maneuvers_frame") // Fenêtre de création d'une manoeuvre

let maneuver_type_selector = document.querySelector("#maneuvers_panel") // Selectionneur du type de manoeuvre
maneuver_type_selector.addEventListener("change", LambertProblemParameters) // [LISTENER] Création du listener appelant la fonction LambertProblemParameters à chaque modif du type de manoeuvre


// ---------------------------------------------------------------------------------------------------------------------------------------------

/* Définition des fonctions gérant les différents affichages permettant le paramétrage de manoeuvres : 
		. Affichage du créateur ou de l'invite de création de manoeuvre (switch)
		. Affichage ou non des paramètres spécifiques au problème de Lambert 	 */


function openCreator () {
	// Remplacement du cadre d'invite à la création de manoeuvre par le cadre de paramétrage de manoeuvre 
	// Appelée au clique sur le bouton "Ajouter une manoeuvre"

	maneuvers_frame_.classList.replace("invite", "creation")
	open_creator_button_.style.display = "none";
	creator_frame.style.display = "block";
}

function closeCreator () {
	// Remplacement du cadre de paramétrage de manoeuvre par le cadre d'invite à la création de manoeuvre
	// Appelée au clique sur le bouton de validation d'un paramétrage de manoeuvre par la fonction addManeuver

	maneuvers_frame_.classList.replace("creation", "invite")
	open_creator_button_.style.display = "block";
	creator_frame.style.display = "none";
}

function LambertProblemParameters () {
	// Affichage du paramétrage d'un problème de Lambert (différent d'un paramétrage de manoeuvre classique) dans le cadre de création de manoeuvre
	// Appelée à la sélection du type "problème de Lambert" dans le cadre "maneuver type"

	if(document.querySelector("#first_line #maneuvers_panel").value == "rdv") {
		document.querySelector("#classic_third_line").style.display = "none"
		document.querySelector("#Lambert_third_line").style.display = "block"
	}

	else {
		document.querySelector("#classic_third_line").style.display = "block"
		document.querySelector("#Lambert_third_line").style.display = "none"
	}
}


// ---------------------------------------------------------------------------------------------------------------------------------------------

/* Gestion de l'ajout de nouvelles manoeuvres ou de nouveaux satellites une fois les formulaires remplies */


let sat_list = [], sat_dict = {},
	man_list = [], man_dict = {}


function addManeuver () {
	//   LECTURE & ENREGISTREMENT d'une manoeuvre rentrée dans le cadre de création de manoeuvre
	// . Récupération d'un paramétrage de manoeuvre via lecture du fichier index.html & réinitialisation des champs 
	// . Création d'un dictionnaire contenant la manoeuvre 
	// . Ajout de ce dictionnaire à la liste de manoeuvre attachée au satellite en cours de création
	// . Passage du mode création au mode invite dans le cadre de manoeuvres


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
	}

	else 
		value_ = document.querySelector("#classic_third_line #maneuver_value")

	let x_dir_ = document.querySelector("#fourth_line #x_dir"),
		y_dir_ = document.querySelector("#fourth_line #y_dir"),
		z_dir_ = document.querySelector("#fourth_line #z_dir")

	man_dict["man_name"] = type_.value
	man_dict["name"] = name_.value 
	man_dict["trigger_type"] = trigger_type_.value
	if(man_dict["trigger_type"] == "angle")
		man_dict["trigger_value"] = Number(trigger_value_.value)
	else
		man_dict["trigger_value"] = trigger_value_.value

	if(type_.value == "rdv") 
		man_dict["value"] = [arvl_date_.value, [Number(x_arvl_.value), Number(y_arvl_.value), Number(z_arvl_.value)]]
	else
		man_dict["value"] = Number(value_.value)
	man_dict["direction"] = [Number(x_dir_.value), Number(y_dir_.value), Number(z_dir_.value)]

	// Réinitialisation des champs HTML

	if(type_.value == "rdv") {
		arvl_date_.value = null
		x_arvl_.value = null
		y_arvl_.value = null
		z_arvl_.value = null
	}

	else 
		value_.value = null

	type_.value = "custom acceleration"
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

	open_creator_button_.style.display = "block"
	creator_frame.style.display = "none"
	maneuvers_frame_.classList.replace("creation", "invite")

	// Fermeture de la fenêtre de création de manoeuvre

	closeCreator()

}

function addSatellite () {
	//   LECTURE & ENREGISTREMENT d'un satellite rentré dans le cadre de création de satellite + les manoeuvre qui lui sont attachées
	// . Récupération d'un paramétrage de satellite via lecture du fichier index.html & réinitialisation des champs 
	// . Création d'un dictionnaire contenant le satellite
	// . Ajout des manoeuvres contenant dans la variable man_list aux manoeuvres du satellite 
	// . Ajout de ce dictionnaire à la liste de satellites


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
	sat_dict["mass"] = Number(mass_.value)
	sat_dict["corps_ref"] = ref_body_.value 
	sat_dict["surface"] = Number(surface_.value)
	sat_dict["r0"] = [Number(xi_.value), Number(yi_.value), Number(zi_.value)]
	sat_dict["v0"] = [Number(vxi_.value), Number(vyi_.value), Number(vzi_.value)]

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


	// Envoie de la nouvelle liste de satellites à la partie exploitation pour l'affichage
	exploitation.newSatellite(sat_list)
}


// ---------------------------------------------------------------------------------------------------------------------------------------------

/* Définition des fonctions communiquantes avec les autres parties du programme */ 


module.exports = 
{
	sendSatellites : function sendSatellites () {
		// Envoie de la liste "sat_list"

		return sat_list},

	addSatelliteFromFile : function addSatelliteFromFile (sat_dict_from_file) {
		// Charge des satellites depuis une liste passée en argument, lue sur un fichier local

		// Ajout du nouveau satellite dans la liste des satellites
		sat_list.push(sat_dict_from_file)

		// Ajout du nouveau satellite dans la liste HTML
		var sat_name_parag = document.createElement("p")
		sat_name_parag.classList.add("text")
		sat_name_parag.classList.add("medium")
		sat_name_parag.style.fontSize = "1.5em"
		sat_name_parag.innerHTML = sat_dict_from_file["name"]
		sat_name_parag.style.marginTop = "10px"
		sat_name_parag.style.marginBottom = "5px" 

		var inner_div_list = []

		for (var i=0 ; i<sat_dict_from_file["maneuvers"].length ; i++) {

			var inner_div = document.createElement("div")
			inner_div.style.display = "flex"
			inner_div.style.marginLeft = "60px"

			let man_name_parag = document.createElement("p")
			sat_name_parag.classList.add("text")
			sat_name_parag.classList.add("medium")
			man_name_parag.style.fontSize = "0.8em"
			man_name_parag.innerHTML = sat_dict_from_file["maneuvers"][i]["name"]

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

		// Envoie de la nouvelle liste de satellites à la partie exploitation pour l'affichage
		exploitation.newSatellite(sat_list)
	}
}