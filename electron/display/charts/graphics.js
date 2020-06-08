function graphicsDisplayer (data_dict) {
	
	document.querySelector("#welcome_panel").style.display = "none"
	document.querySelector("#graph_visual").style.display = "block"

	var n_graphs = Object.keys(data_dict).length

	var graphics_div = document.querySelector("#graph_visual")

	// Ajout de la légend
	let div_ = document.createElement('div')
	div_.id = "legend"
	document.querySelector("#graph_visual").appendChild(div_)
	makeLegend(data_dict)

	// Ajout des graphes
	for (var i=0 ; i<n_graphs ; i++) {
		let div_ = document.createElement('div')
		div_.id = "frame-"+i+""
		document.querySelector("#graph_visual").appendChild(div_)
		makeUnitGraph(Object.keys(data_dict)[i], data_dict[Object.keys(data_dict)[i]], i, n_graphs)
	}

}

function makeLegend (data_dict) {
	let names = []
	// Récupération des noms des satellites
	for (const attr in data_dict) {
		for (var i=0 ; i<data_dict[String(attr)].length ; i++) {
  			if(!(names.indexOf(data_dict[String(attr)][i].name) > -1))
				names.push(data_dict[String(attr)][i].name)
		}
	}

	var margin = {top: 10, right: 10, bottom: 10, left: 10},
	    width = 300 - margin.left - margin.right,
	    height = 100 - margin.top - margin.bottom

	var svg = d3.select("#legend")
				.append("svg")
			    .attr("width", width + margin.left + margin.right)
			    .attr("height", height + margin.top + margin.bottom)
			    .append("g")
			    .attr("transform", "translate(" + margin.left + "," + margin.top + ")")
			    	.selectAll('g')
			  		.data(names)
			  		.enter()
					.append('g')

	svg.append('rect')
					.attr("class", (d, i) => {return "line-"+i+" line"})
					// .attr('fill', (d, i) => {return "lightgreen"})
					.attr('width', 30)
					.attr('height', 1)
					.attr('x', 0)	
					.attr('y', (d, i) => {return 15*i;})

	svg.append("text")
					.attr("class", "legend")
	  				.attr("dx", 40)
	  				.attr("dy", 4)
	  				.style("text-anchor", "start")
	  				.text((d, i) => {console.log(names[i]); return names[i]}) 
	  				.attr('x', 0)	
					.attr('y', (d, i) => {return 15*i;})

}

function makeUnitGraph (prm_name, orb_parm_data, num, n_graphs) {

	let concat_values = orb_parm_data[Object.keys(orb_parm_data)[0]].vals

	let id = 0
	const ids = function () {
	    return "line-"+(id++) }


	var margin = {top: 30, right: 150, bottom: 30, left: 100},
	    width = 1300 - margin.left - margin.right,
	    height = (650/n_graphs) - margin.top - margin.bottom

	var svg = d3.select("#frame-"+num+"")
			    .append("svg")
			    .attr("width", width + margin.left + margin.right)
			    .attr("height", height + margin.top + margin.bottom)
			    .append("g")
			    .attr("transform", "translate(" + margin.left + "," + margin.top + ")")
 
	for (var i=1 ; i<Object.keys(orb_parm_data).length ; i++) {
		concat_values = concat_values.concat(orb_parm_data[Object.keys(orb_parm_data)[i]].vals) }


	// X - axis
	var x_scale = d3.scaleLinear() 
			  .range([ 0, width ]) // Indique la transformation a apporter aux données pour faire la convertion : valeur <-> coordonnées en abcisse
			  .domain(d3.extent(concat_values, d => d.time ))  // Indique la range des valeurs prises sur l'axe des abcisses

	const xaxis = svg.append("g")
	  .attr("class", "axis") 
      .attr("transform", "translate(0," + height + ")")
      .call(d3.axisBottom(x_scale))


	// Y - axis
	var y_scale = d3.scaleLinear()
		.range([ height, 0 ]) // Indique la transformation a apporter aux données pour faire la convertion : valeur <-> coordonnées en ordonnée
	    .domain([d3.min(concat_values, d => d.value), d3.max(concat_values, d => d.value)])  // Indique la range des valeurs prises sur l'axe des ordonnées

	const yaxis = svg.append("g")
	  .attr("class", "axis") 
      .call(d3.axisLeft(y_scale))
	  .append("text")
	  .attr("dy", "-1.1em")
	  .attr("y", 6)
	  .style("text-anchor", "start")
	  .text(prm_name);


	var clip = svg.append("defs").append("svg:clipPath")
        .attr("id", "clip")
        .append("svg:rect")
        .attr("width", width )
        .attr("height", height )
        .attr("x", 0)
        .attr("y", 0);

	const line = d3.line()
    .x(function(d) { return x_scale(d.time) })
    .y(function(d) { return y_scale(d.value) })

	const lines = svg.append('g')
      .attr("clip-path", "url(#clip)")
      .selectAll("lines") // sélection de toutes les lignes (création en réalité ...)
      .data(orb_parm_data) // liaison avec les données
   	  .enter() 
   	  .append("g"); // création de nouvelles balises "g" pour liées à chaque tableaux de données
 	
 	lines.append("path")
 	 .attr("class", (d, i) => {return "line-"+i+" line"})
	 .attr("d", (d) => { return line(d.vals); } )

    lines.append("text")
    .attr("class","serie_label")
    .datum((d) => { 
        return { name: d.name, vals: d.vals[d.vals.length - 1]}; })
    .attr("transform", function(d) { 
            return "translate(" + (x_scale(d.vals.time) + 0)  
            + "," + (y_scale(d.vals.value) + 5 ) + ")";})
    .attr("x", 5)
    .text(function(d) { return d.name; });

    let brush = d3.brushX() 
    .extent( [ [0,0], [width,height] ] )
    .on("end", updateChart) 

	d3.select('#frame-'+num+' g[clip-path="url(#clip)"]').append("g")
    	.attr("class", "brush")
    	.call(brush);


    var idleTimeout
	function idled() { idleTimeout = null; }

	// A function that update the chart for given boundaries
	function updateChart() {

	   // Selected boundaries
	   extent = d3.event.selection

	   // If no selection, back to initial coordinate. Otherwise, update X axis domain
	   if(!extent){
	     if (!idleTimeout) return idleTimeout = setTimeout(idled, 350); // This allows to wait a little bit
	     x_scale.domain([4,8])
	   }else{
	     x_scale.domain([ x_scale.invert(extent[0]), x_scale.invert(extent[1]) ])
	     d3.select('#frame-'+num+' g[clip-path="url(#clip)"]').select(".brush").call(brush.move, null) // This remove the grey brush area as soon as the selection has been done
	   }

	   // Update axis and line position
	   xaxis.transition().duration(400).call(d3.axisBottom(x_scale))

	   lines.select('.line')
	        .transition()
	        .duration(400)
	        .attr("d", (d) => { return line(d.vals); } )
	 }


	 // If user double click, reinitialize the chart
	svg.on("dblclick",function(){
	  x_scale.domain(d3.extent(concat_values, function(d) { return d.time; }));

	  xaxis.transition().call(d3.axisBottom(x_scale));

	  lines.select('.line')
	    .transition()
	    .attr("d", (d) => { return line(d.vals); } )
	}); 

}


module.exports.graphicsDisplayer = graphicsDisplayer