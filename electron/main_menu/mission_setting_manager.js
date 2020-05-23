const BrowserWindow = require('electron').remote.BrowserWindow
const { ipcRenderer } = require("electron")

var new_simulation_btn = document.querySelector(".prg_launch")
new_simulation_btn.addEventListener("click", () => {createNewSimulationWindow("Comparaison masses")})

var new_simulation_window // variable contenant la fenêtre de paramétrage mission

function createNewSimulationWindow (mission_to_load) {
	const general_display = require("../display/general_display.js")

	new_simulation_window = new BrowserWindow({width: 1200,height: 600, frame:false, webPreferences: {nodeIntegration: true}})
	new_simulation_window.loadFile('./electron/mission_setting/index.html')
	// new_simulation_window.webContents.openDevTools()

	// Envoie du nom de la mission à charger
	new_simulation_window.webContents.once('dom-ready', () => {
		BrowserWindow.getAllWindows()[0].send("mission_to_load", mission_to_load)
		general_display.missionSettingInProgress()
	});

	general_display.missionSettingInProgress()

	ipcRenderer.on("hand again", (event, prm_dict) => {
		/* Quand le paramétrage de la mission est terminé, on stock l'objet dans le dossier "historic" 
			et on l'envoie au moteur de calcul pour lancer la simulation */ 

		general_display.missionSettingDone()


		const fs  = require('fs')
		fs.writeFile("./electron/historic/"+ prm_dict.general["mission name"] +".json", JSON.stringify(prm_dict), (err) => {
	    	if (err) 
        		console.error(err) })

		historicManager() // mise à jour de l'historique

		let pythonShell = require("../data_processing/python_shell.js")
		pythonShell.sendPythonShell(prm_dict)
	})
}


function historicManager () {

	const fs = require('fs');

	var div_ = document.querySelector("#annex_displayer")
	var ol_ = document.createElement("ul")

	fs.readdir('./electron/historic' , (err, files) => {
		
	for (var i=1 ; i<files.length ; i++) {

		var name = document.createElement("a")
		name.href = "#"
		name.innerHTML = files[i].replace(".json", "")
		name.classList.add("historic_cell_text")

		var li_ = document.createElement("li")
		li_.appendChild(name)
		li_.style.color = "white"
		li_.style.marginBottom = "10px"

		ol_.appendChild(li_) 	}
	  
	  div_.appendChild(ol_)			});
}
