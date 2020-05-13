const BrowserWindow = require('electron').remote.BrowserWindow

/* DATE SETTING */

var currentUTC = document.querySelector(".currentUTC")
var date = new Date()

currentUTC.innerHTML = date.toUTCString()

function setDate () {
	date = new Date()
	currentUTC.innerHTML = date.toUTCString()
	setTimeout(setDate, 1000)
}
setDate()

/* ANNEX PANEL MANAGEMENT */
var annex_ = document.querySelector("#annex")
var annexDisplayer_ = document.querySelector(".annex_displayer")
annex_.addEventListener("change", ()=>{
	getHistoricList()
})

function getHistoricList () {

}


/* LAUNCH NEW PROGRAM MANAGER */

var pgr_launcher_btn = document.querySelector(".prg_launch")
pgr_launcher_btn.addEventListener("click", () => {
	document.querySelector("html").style.filter = "blur(2px)"
	let pgr_lancher_win = new BrowserWindow({width: 1200,height: 600, frame:false, webPreferences: {nodeIntegration: true}})
	pgr_lancher_win.loadFile('./electron/mission_setting/index.html')
	pgr_lancher_win.webContents.openDevTools()
})


