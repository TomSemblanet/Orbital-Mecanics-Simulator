/* Création du dictionnaire contenant les paramètres de la section "general" par lecture des champs
	dans le fichier index.html */

var parameters_dict = {} // dictionnaire global "general"

function buildParametersDict () {
	// Lecture des champs dans le fichier index.html et ajout au dictionnaire parameters_dict

	let mission_name_ = document.querySelector("#mission_name")
	parameters_dict["mission name"] = mission_name_.value

	let dpt_date_ = document.querySelector("#departure_date")
	parameters_dict["starting date"] = dpt_date_.value

	let end_date_ = document.querySelector("#end_date")
	parameters_dict["end date"] = end_date_.value

	let dt_ = document.querySelector("#dt")
	parameters_dict["time step"] = dt_.value

	let perturbations_ = document.querySelectorAll(".perturbations"),
		perturbations_list = []
	for (var i=0 ; i<perturbations_.length ; i++) {
		if(perturbations_[i].checked == true)
			perturbations_list.push(perturbations_[i].name)
	}
	parameters_dict["perturbations"] = perturbations_list

	let ephemerides_file_ = document.querySelector("#ephemerides")
	parameters_dict["ephemerides file"] = ephemerides_file_.value
}

// [LISTENER] Création du listener appelant la fonction de mise-à-jour du dictionnaire de paramétrage à chaque modification
// 				de la page
document.querySelector("#generals").addEventListener("change", buildParametersDict) 


// ---------------------------------------------------------------------------------------------------------------------------------------------

/* Définition des fonctions communiquantes avec les autres parties du programme */ 

module.exports = 
{
	sendGeneralsPrm : function sendGeneralsPrm () {
		// Envoie de le dictionnaire de paramètres "general"

		return parameters_dict},

	loadGeneralsFromFile : function loadGeneralsFromFile (dict_from_file) {
		// . Lecture des paramètres "general" dans un dictionnaire pré-chargé et affectations des valeurs au champs dans le fichier index.html
		// . Création et remplissage du dictionnaire parameters_dict contenant les paramètres "general"

		let mission_name_ = document.querySelector("#mission_name")
		mission_name_.value = dict_from_file["general"]["mission name"]

		let dpt_date_ = document.querySelector("#departure_date")
		dpt_date_.value = dict_from_file["general"]["starting date"]

		let end_date_ = document.querySelector("#end_date")
		end_date_.value = dict_from_file["general"]["end date"]

		let dt_ = document.querySelector("#dt")
		dt_.value = dict_from_file["general"]["time step"]

		let perturbations_ = document.querySelectorAll(".perturbations"),
			perturbations_list = dict_from_file["general"]["perturbations"]

		for (var i=0 ; i<perturbations_list.length ; i++) {
			for (var j=0 ; j<perturbations_.length ; j++) {
				if (perturbations_[j].name == perturbations_list[i])
					perturbations_[j].checked = true
			}
		}

		let ephemerides_file_ = document.querySelector("#ephemerides")
		ephemerides_file_.value = dict_from_file["general"]["ephemerides file"]


		parameters_dict = dict_from_file["general"] // Création du dictionnaire contenant les paramètres "general"
	}
}
