/* DATE SETTING */
var currentUTC = document.querySelector(".currentUTC"), date
setDate()

function setDate () {
	date = new Date()
	currentUTC.innerHTML = date.toUTCString()
	setTimeout(setDate, 1000) }

const historic_manager = require("./historic_manager")
historic_manager.historicManager()