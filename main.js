const electron = require('electron')
const app = electron.app
const BrowserWindow = electron.BrowserWindow
const { ipcMain } = require('electron')


let window_

function createWindow () {

	window_ = new BrowserWindow({width: 1440,height: 900, webPreferences: {nodeIntegration: true}})
	window_.loadFile('./electron/main_menu/index.html')
	// window_.webContents.openDevTools()
}

app.whenReady().then(createWindow)

app.on('window-all-closed', () => {
	if(process.platform !== 'darwin') {
		app.quit()
	}
})

ipcMain.on("prm_window_closing", (event, prm_dict) => {
	/* Détecte la fermeture de la fenêtre de paramétrage mission une fois que le fichier .json
	   correspondant a été crée et informe la fenêtre principale qu'elle a à nouveau la main via IPC */ 

	window_.send("hand again", prm_dict)
})

// ipcMain.on("mission_to_load", (event, mission_to_load) => {
// 	/* Envoie au module 'mission_setting' le nom du fichier .json à pré-charger pour le paramétrage
// 		de la mission */
// 	console.log(BrowserWindow.getAllWindows())
// 	BrowserWindow.getAllWindows()[0].send("mission_to_load", mission_to_load)
// 	// window_.send("mission_to_load", mission_to_load)
// 	// console.log(mission_to_load)
// }) 