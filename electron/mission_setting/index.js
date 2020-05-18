/* Gestion de l'affichage et du masquage des fenêtres de paramétrage en fonction du 
 clique sur les boutons "GÉNÉRAL", "SATELLITES", "CORPS CÉLESTES" et "EXPLOITATION" dans le header */

const BrowserWindow = require('electron').remote.BrowserWindow
const { ipcRenderer } = require("electron")

var header_buttons = document.querySelectorAll(".frame"), // sélection des boutons dans le header
	prm_windows = document.querySelectorAll(".prm_window") // sélection de la fenêtre principale où s'affichent les fenêtres

var curr_frame_ind = 0 

function setCurrentFrame () { 
	// gestion de l'affichage et du masquage des fenêtres en fonction de la selection de l'utilisateur

	for(var i=0 ; i<4 ; i++) {
		if(i == curr_frame_ind && (prm_windows[i].style.display == "none")) 
			prm_windows[i].style.display = "block"
		else if (i != curr_frame_ind && prm_windows[i].style.display == "block") 
			prm_windows[i].style.display= "none"
	}
}

// [LISTENER] Ajout des listeners à l'appuie sur les boutons "GÉNÉRAL", "SATELLITES", "CORPS CÉLESTES" et "EXPLOITATION" dans le header
header_buttons[0].addEventListener("click", () => {curr_frame_ind = 0; setCurrentFrame()}) 
header_buttons[1].addEventListener("click", () => {curr_frame_ind = 1; setCurrentFrame()})
header_buttons[2].addEventListener("click", () => {curr_frame_ind = 2, setCurrentFrame()})
header_buttons[3].addEventListener("click", () => {curr_frame_ind = 3, setCurrentFrame()})

// ---------------------------------------------------------------------------------------------------------------------------------------------

/* Gestion de de la recéption des paramètres des fichiers
		. generals.js
		. satellites.js
		. celestial_bodies.js
		. exploitation.js      
	et envoie du dictionnaire de paramétrage au moteur de calcul via le shell Python */


// Inclusion des dépendances
var generals = require("./generals.js"),
	satellites = require("./satellites.js"),
	celestial_bodies = require("./celestial_bodies.js"),
	exploitation = require("./exploitation.js")


var mission_validation_ = document.querySelector("#mission_validation") // bouton de validation de mission

// [LISTENER]
mission_validation_.addEventListener("click", simulationLaunch)

function simulationLaunch () {
	// . Réception des paramétrages de mission
	// . Création du dictionnaire général de mission
	// . Envoie du dictionnaire de paramétrage à la fenêtre principale

	var generals_prm_getter = generals.sendGeneralsPrm(),
		satellites_getter = satellites.sendSatellites(),
		celestial_bodies_getter = celestial_bodies.sendCelestialBodies(),
		renderer_getter = exploitation.sendExploitation()

	let final_mission_dict = {
		"creation date" : new Date().toUTCString(),
		"generals" : generals_prm_getter,
		"celestial bodies" : celestial_bodies_getter,
		"satellites" : satellites_getter,
		"exploitation" : renderer_getter
	}


	document.querySelector("#settings").style.opacity = "0"
	document.querySelector("#confirm").style.display = "inline"
	
	setTimeout(() => {document.querySelector("#confirm").style.opacity = "1"}, 300)

	setTimeout(() => {
		ipcRenderer.send("prm_window_closing", final_mission_dict)
		window.close()
	}, 1500)

	// ipcRenderer.send("prm_window_closing")

	// let pythonShell = require("./python_shell.js")
	// pythonShell.sendPythonShell(final_mission_dict)
}

// ---------------------------------------------------------------------------------------------------------------------------------------------

/* Appel de la fonction de pré-remplissage des champs HTML pour le chargement du paramétrage d'une mission */

var mission_loader = require("./load_mission.js")
mission_loader.missionLoader('example')

