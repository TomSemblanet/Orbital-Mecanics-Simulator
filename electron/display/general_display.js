function removeHeader () {
	document.querySelector("#header").style.display = "none"
	document.querySelector(".main_panel").style.height = "700px"
	document.querySelector(".annex_panel").style.height = "700px"
}

function showHeader () {
	document.querySelector("#header").style.display = "block"
	document.querySelector(".main_panel").style.height = "650px"
	document.querySelector(".annex_panel").style.height = "650px"
}

function accelerateCircles () {
	document.querySelector("#b").classList.replace("normal", "speed")
	document.querySelector("#g").classList.replace("normal", "speed")
	document.querySelector("#y").classList.replace("normal", "speed")
	document.querySelector("#r").classList.replace("normal", "speed")
}

function slowCircles () {
	document.querySelector("#b").classList.replace( "speed", "normal")
	document.querySelector("#g").classList.replace( "speed", "normal")
	document.querySelector("#y").classList.replace( "speed", "normal")
	document.querySelector("#r").classList.replace( "speed", "normal")
}

function cleanMainPanel () {
	document.querySelector(".logo").style.display = "none"
	document.querySelector(".orbit").style.display = "none"
	document.querySelector(".prg_launch").style.display = "none"
} 



function missionSettingInProgress () {
	document.querySelector("html").style.filter = "blur(5px)"
	removeHeader()
}

function missionSettingDone () {
	accelerateCircles()
	cleanMainPanel()

	document.querySelector("html").style.filter = "blur(0px)"
}

module.exports.missionSettingInProgress = missionSettingInProgress
module.exports.missionSettingDone = missionSettingDone