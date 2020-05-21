const BrowserWindow = require('electron').remote.BrowserWindow
const { ipcRenderer } = require("electron")

var new_simulation_btn = document.querySelector(".prg_launch")
new_simulation_btn.addEventListener("click", createNewSimulationWindow)

var new_simulation_window // variable contenant la fenêtre de paramétrage mission

function createNewSimulationWindow () {
	const general_display = require("../display/general_display.js")

	new_simulation_window = new BrowserWindow({width: 1200,height: 600, frame:false, webPreferences: {nodeIntegration: true}})
	new_simulation_window.loadFile('./electron/mission_setting/index.html')
	new_simulation_window.webContents.openDevTools()

	general_display.missionSettingInProgress()

	ipcRenderer.on("hand again", (event, prm_dict) => {
		/* Quand le paramétrage de la mission est terminé, on stock l'objet dans le dossier "historic" 
			et on l'envoie au moteur de calcul pour lancer la simulation */ 

		general_display.missionSettingDone()


		const fs  = require('fs')
		fs.writeFile("./electron/historic/"+ prm_dict.generals["mission name"] +".json", JSON.stringify(prm_dict), (err) => {
	    	if (err) 
        		console.error(err) })

		let pythonShell = require("../data_processing/python_shell.js")
		pythonShell.sendPythonShell(prm_dict)
	})
}
