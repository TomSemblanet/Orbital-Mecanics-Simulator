var parameters_dict = {}

function loadParameters () {

	// Ajout des éléments HTML au dictionnaire parameters_dict

	let mission_name_ = document.querySelector("#mission_name")
	parameters_dict["mission name"] = mission_name_.value

	let dpt_date_ = document.querySelector("#departure_date")
	parameters_dict["dpt date"] = dpt_date_.value

	let end_date_ = document.querySelector("#end_date")
	parameters_dict["end date"] = end_date_.value

	let dt_ = document.querySelector("#dt")
	parameters_dict["dt"] = dt_.value

	let perturbations_ = document.querySelectorAll(".perturbations"),
		perturbations_list = []
	for (var i=0 ; i<perturbations_.length ; i++) {
		if(perturbations_[i].checked == true)
			perturbations_list.push(perturbations_[i].name)
	}
	parameters_dict["perturbations"] = perturbations_list

	let ephemerides_file_ = document.querySelector("#ephemerides")
	parameters_dict["ephemerides file"] = ephemerides_file_.value
}

document.querySelector("html").addEventListener("change", loadParameters)

module.exports = 
{
	send_generals_prm : function send_generals_prm () {return parameters_dict}
}
