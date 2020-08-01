function FeatureManager(divId) {
    this.div = "#" + divId;
}

FeatureManager.prototype.plotFeatures = function(features) {
    $(this.div + " svg").remove();
    $("#colormap").hide();

    // set the dimensions and margins of the graph
    var margin = {top: 30, right: 30, bottom: 30, left: 30},
      width = $(this.div).width() - margin.left - margin.right,
      height = $(this.div).height() - margin.top - margin.bottom;

    // append the svg object to the body of the page
    var svg = d3.select(this.div)
    .append("svg")
      .attr("width", width + margin.left + margin.right)
      .attr("height", height + margin.top + margin.bottom)
    .append("g")
      .attr("transform",
            "translate(" + margin.left + "," + margin.top + ")");

    // Labels of row and columns
    var myGroups = features["xlabels"]
    var myVars = features["ylabels"]
    var myData = features["fcs"];
    var data = []
    for ( var i=0; i < myVars.length; i++ )
        for ( var j=0; j < myGroups.length; j++ )
            data.push({'emotion': myGroups[j], 'feature': myVars[i], 'val': myData[i][j]})

    // Build X scales and axis:
    var x = d3.scaleBand()
      .range([ 0, width*0.75 ])
      .domain(myGroups)
      .padding(0.01);
    svg.append("g")
      .attr("transform", "translate(0," + height + ")")
      .call(d3.axisBottom(x))

    // Build X scales and axis:
    var y = d3.scaleBand()
      .range([ height, 0 ])
      .domain(myVars)
      .padding(0.01);
    svg.append("g")
      .attr("transform", "translate(" + (width*0.75) + ", 0)")
      .call(d3.axisRight(y));

    // Build color scale
    var myColor = d3.scaleSequential(d3.interpolateRdBu).domain([-1,1])

    svg.selectAll()
          .data(data, function(d) {return d.emotion+':'+d.feature;})
          .enter()
          .append("rect")
          .attr("x", function(d) { return x(d.emotion) })
          .attr("y", function(d) { return y(d.feature) })
          .attr("width", x.bandwidth() )
          .attr("height", y.bandwidth() )
          .style("fill", function(d) { return myColor(d.val)} )
    $("#colormap").show();
}