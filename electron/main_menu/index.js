var currentUTC = document.querySelector(".currentUTC")
var date = new Date();

currentUTC.innerHTML = date.toUTCString()

function setDate () {
	date = new Date()
	currentUTC.innerHTML = date.toUTCString()
	setTimeout(setDate, 1000)
}

setDate()


var annex_ = document.querySelector("#annex")
var annexDisplayer_ = document.querySelector(".annex_displayer")
annex_.addEventListener("change", ()=>{
	console.log(annex_.value)
	annexDisplayer_.innerHTML = annex_.value
	annexDisplayer_.style.color = "white"
	annexDisplayer_.style.fontFamily = "CMU Serif"
	annexDisplayer_.style.fontSize = "1.5em"
})

var hist_msn_names = []

function getHistoricList () {
	let jsonData = require('../historic/template.json');
	for (var i=0 ; i < jsonData["historic"].length ; i++) {
	console.log(jsonData["historic"][i]["general"]["mission name"]);
	console.log("\t"+jsonData["historic"][i]["creation_date"])
	}
}

getHistoricList()