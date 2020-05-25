module.exports.historicManager =  function historicManager () {

	const fs = require('fs');

	var div_ = document.querySelector("#annex_displayer")
	var ul_ = document.createElement("ul")
	ul_.id = "historic_list"

	fs.readdir('./electron/historic' , (err, files) => {
		
	for (var i=1 ; i<files.length ; i++) {

		if(files[i] != "empty_mission.json") {

		let file_ = require('../historic/'+files[i]) 

		var cr_date = document.createElement('p')
		cr_date.innerHTML = file_["creation date"].replace(" GMT", "")
		cr_date.classList.add("historic_date")

		// Ajout du lien contenant le nom de la mission
		var name = document.createElement("a")
		name.href = "#"
		name.innerHTML = files[i].replace(".json", "")
		name.classList.add("historic_cell_text")

		// Ajout de l'élément à la balise <ul>
		var li_ = document.createElement("li")
		li_.appendChild(name)
		li_.appendChild(cr_date)

		ul_.appendChild(li_) 	
	 } }
	  
	  div_.appendChild(ul_)			
	});
}

module.exports.clearHistoric = function clearHistoric () {
	var div_ = document.querySelector("#annex_displayer"), 
		ul_to_remove = document.querySelector("#annex_displayer ul")

	div_.removeChild(ul_to_remove)

}