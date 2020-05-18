const electron = require('electron')
const app = electron.app
const BrowserWindow = electron.BrowserWindow
const { ipcMain } = require('electron')


let window_

function createWindow () {

	window_ = new BrowserWindow({width: 1440,height: 900, webPreferences: {nodeIntegration: true}})
	window_.loadFile('./electron/main_menu/index.html')
	window_.webContents.openDevTools()
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