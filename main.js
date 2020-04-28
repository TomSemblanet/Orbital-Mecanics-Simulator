const electron = require('electron')
const app = electron.app
const BrowserWindow = electron.BrowserWindow

function createWindow () {

	let window_ = new BrowserWindow({width: 800,height: 600, webPreferences: {nodeIntegration: true}})
	window_.loadFile('./electron/index.html')
	window_.webContents.openDevTools()
}

app.whenReady().then(createWindow)

app.on('window-all-closed', () => {
	if(process.platform !== 'darwin') {
		app.quit()
	}
})