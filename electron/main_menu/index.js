/* DATE SETTING */
var currentUTC = document.querySelector(".currentUTC"), date
setDate()

function setDate () {
	date = new Date()
	currentUTC.innerHTML = date.toUTCString()
	setTimeout(setDate, 1000) }