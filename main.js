const electron = require('electron')
const app = electron.app
const BrowserWindow = electron.BrowserWindow

function createWindow () {

	let window_ = new BrowserWindow({width: 1440,height: 900, webPreferences: {nodeIntegration: true}})
	window_.loadFile('./electron/main_menu/index.html')
	window_.webContents.openDevTools()
}

app.whenReady().then(createWindow)

app.on('window-all-closed', () => {
	if(process.platform !== 'darwin') {
		app.quit()
	}
})