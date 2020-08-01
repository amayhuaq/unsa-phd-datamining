function CircumplexManager(divId) {
    this.div = "#" + divId;
}

CircumplexManager.prototype.plotPoints = function(points) {
    $(this.div + " svg").remove();

    // set the dimensions and margins of the graph
    var margin = {top: 10, right: 10, bottom: 10, left: 10},
        width = $(this.div).height() - margin.left - margin.right,
        height = $(this.div).height() - margin.top - margin.bottom;

    // append the svg object to the body of the page
    var svg = d3.select(this.div)
      .append("svg")
        .attr("width", "100%")
        .attr("height", "100%")
      .append("g")
        .attr("transform",
              "translate(" + ($(this.div).width()/2 - $(this.div).height()/2) + "," + margin.top + ")");

    //Read the data
    // Add X axis
      var x = d3.scaleLinear()
        .domain([1, 9])
        .range([ 0, width ]);
      svg.append("g")
        .attr("transform", "translate(0," + height/2 + ")")
        .call(d3.axisBottom(x));

      // Add Y axis
      var y = d3.scaleLinear()
        .domain([1, 9])
        .range([ height, 0]);
      svg.append("g")
        .attr("transform", "translate(" + width/2 + ", 0)")
        .call(d3.axisLeft(y));

      // Color scale: give me a specie name, I return a color
      var color = d3.scaleOrdinal()
        .domain([0, 1, 2, 3 ])
        .range([ "#440154ff", "#21908dff", "#fde725ff", "#ff0005ff"])

      // Add dots
      svg.append('g')
        .selectAll("dot")
        .data(points)
        .enter()
        .append("circle")
          .attr("cx", function (d) { return x(d.valence); } )
          .attr("cy", function (d) { return y(d.arousal); } )
          .attr("r", 3)
          .style("fill", function (d) { return color(d.emotion); } )
}
