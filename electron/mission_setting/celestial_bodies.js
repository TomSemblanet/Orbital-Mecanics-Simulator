/* Création du dictionnaire contenant les paramètres de la section "celestial bodies" par lecture des champs
	dans le fichier index.html */

var celestial_bodies_dict = {"to load" : []} // dictionnaire global "celestial bodies"

function buildCelestialBodiesDict () {
	// Lecture des champs dans le fichier index.html et ajout au dictionnaire celestial_bodies_dict 

	celestial_bodies_names = []

	let box_list_ = document.querySelectorAll("#celestial_bodies input")

	for(var i=0 ; i<box_list_.length ; i++) {
		if(box_list_[i].checked == true) 
			celestial_bodies_names.push(box_list_[i].name)
	}

	celestial_bodies_dict["to load"] = celestial_bodies_names
}

// [LISTENER] Création du listener appelant la fonction de mise-à-jour du dictionnaire de paramétrage à chaque modification
// 				de la page
document.querySelector("#celestial_bodies").addEventListener("change", buildCelestialBodiesDict)

// ---------------------------------------------------------------------------------------------------------------------------------------------

/* Définition des fonctions communiquantes avec les autres parties du programme */ 

module.exports = 
{
	sendCelestialBodies : function sendCelestialBodies () {
		// Envoie de le dictionnaire de paramètres "celestial bodies"

		return celestial_bodies_dict},

	loadCelestialBodiesFromFile : function loadCelestialBodiesFromFile(dict_from_file) {
		// . Lecture des paramètres "celestial bodies" dans un dictionnaire pré-chargé et affectations des valeurs au champs dans le fichier index.html
		// . Création et --> remplissage du dictionnaire celestial_bodies_dict <-- contenant les paramètres "celestial bodies"

		let inputs_list_ = document.querySelectorAll("#celestial_bodies input")

		for (var i=0 ; i < dict_from_file["celestial bodies"]["to load"].length ; i++) {
			for (var j=0 ; j < inputs_list_.length ; j++) {
				if (inputs_list_[j].name == dict_from_file["celestial bodies"]["to load"][i])
					inputs_list_[j].checked = true
			}
		}


		celestial_bodies_dict = dict_from_file["celestial bodies"] // Création du dictionnaire contenant les paramètres "celestial bodies"
	}
}