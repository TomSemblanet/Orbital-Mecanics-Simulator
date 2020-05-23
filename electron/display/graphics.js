function graphicsDisplayer (data_dict) {
	
	document.querySelector("#welcome_panel").style.display = "none"
	document.querySelector("#graph_visual").style.display = "block"

	var n_graphs = Object.keys(data_dict).length

	console.log(data_dict)

	for (var i=0 ; i<n_graphs ; i++) {
		makeUnitGraph(Object.keys(data_dict)[i], data_dict[Object.keys(data_dict)[i]], i, n_graphs)
	}

}

function makeUnitGraph (prm_name, orb_parm_data, num, n_graphs) {

	let concat_values = orb_parm_data[Object.keys(orb_parm_data)[0]].vals

	let id = 0
	const ids = function () {
	    return "line-"+(id++) }



	var margin = {top: 30, right: 150, bottom: 30, left: 100},
	    width = 1200 - margin.left - margin.right,
	    height = (650/n_graphs) - margin.top - margin.bottom

	var svg = d3.select("#graph_visual")
			    .append("svg")
			    .attr("width", width + margin.left + margin.right)
			    .attr("height", height + margin.top + margin.bottom)
			    .append("g")
			    .attr("transform", "translate(" + margin.left + "," + margin.top + ")")
 
	for (var i=1 ; i<Object.keys(orb_parm_data).length ; i++) {
		concat_values = concat_values.concat(orb_parm_data[Object.keys(orb_parm_data)[i]].vals) }


	var x_scale = d3.scaleLinear() 
			  .range([ 0, width ]) // Indique la transformation a apporter aux données pour faire la convertion : valeur <-> coordonnées en abcisse
			  .domain(d3.extent(concat_values, d => d.time ))  // Indique la range des valeurs prises sur l'axe des abcisses

	var y_scale = d3.scaleLinear()
		.range([ height, 0 ]) // Indique la transformation a apporter aux données pour faire la convertion : valeur <-> coordonnées en ordonnée
	    .domain([d3.min(concat_values, d => d.value), d3.max(concat_values, d => d.value)])  // Indique la range des valeurs prises sur l'axe des ordonnées


	const yaxis = d3.axisLeft()
				.ticks(5)
				.scale(y_scale)

	const xaxis = d3.axisBottom()
				.scale(x_scale)


	svg.append("g")
	    .attr("class", "axis") 
	    .attr("transform", "translate(0," + height + ")")
	    .call(xaxis)
	    .append("text")
	    .attr("transform", "translate(" + (width+62) + ", 7)")
		.style("text-anchor", "end")
		.text("Temps");

    
	svg.append("g")
	    .attr("class", "axis") 
	    .call(yaxis)
	    .append("text")
		.attr("dy", "-0.5em")
		.attr("y", 6)
		.attr("dx", "1em")
		.style("text-anchor", "end")
		.text(prm_name);

	const line = d3.line()
    .x(function(d) { return x_scale(d.time) })
    .y(function(d) { return y_scale(d.value) })

    const lines = svg.selectAll("lines")
    				 .data(orb_parm_data)
   					 .enter()
   					 .append("g");

  	lines.append("path")
  	.attr("class", ids)
    .attr("d", function(d) { return line(d.vals); });

    lines.append("text")
    .attr("class","serie_label")
    .datum(function(d) { 
        return {
            name: d.name, 
            vals: d.vals[d.vals.length - 1]}; })
    .attr("transform", function(d) { 
            return "translate(" + (x_scale(d.vals.time) + 10)  
            + "," + (y_scale(d.vals.value) + 5 ) + ")";})
    .attr("x", 5)
    .text(function(d) { return d.name; });

}



module.exports.graphicsDisplayer = graphicsDisplayer