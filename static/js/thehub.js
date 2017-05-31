function init_d3() {
  var width = 960;
  var height = 500;

  var color = d3.scale.category10();

  var force = d3.layout.force()
    .charge(-120)
    .linkDistance(30)
    .size([width, height]);

  var x = d3.scale.linear()
    .domain([0, 16])
    .range([250, 80])
    .clamp(true);

  var brush = d3.svg.brush()
    .y(x)
    .extent([0, 0]);

  var svg = d3.select("body").append("svg")
    .attr("width", width)
    .attr("height", height);

  var links_g = svg.append("g");
  var nodes_g = svg.append("g");

  // slider
  svg.append("g")
    .attr("class", "x axis")
    .attr("transform", "translate(" + (width - 20)  + ",0)")
    .call(d3.svg.axis()
      .scale(x)
      .orient("left")
      .tickFormat(function(d) { return d; })
      .tickSize(0)
      .tickPadding(12))
    .select(".domain")
      .select(function() { return this.parentNode.appendChild(this.cloneNode(true)); })
        .attr("class", "halo");

  var slider = svg.append("g")
    .attr("class", "slider")
    .call(brush);

  slider.selectAll(".extent,.resize")
    .remove();

  var handle = slider.append("circle")
    .attr("class", "handle")
    .attr("transform", "translate(" + (width - 20) + ",0)")
    .attr("r", 5);

  svg.append("text")
    .attr("x", width - 15)
    .attr("y", 60)
    .attr("text-anchor", "end")
    .attr("font-size", "12px")
    .style("opacity", 0.5)
    .text("co-occurence threshold")

  d3.json("/characters.json", function(error, graph) {
    if (error) throw error;
    
    graph.links.forEach(function(d,i){ d.i = i; });

    function brushed() {
      var value = brush.extent()[0];

      if (d3.event.sourceEvent) {
        value = x.invert(d3.mouse(this)[1]);
        brush.extent([value, value]);
      }
      handle.attr("cy", x(value));
      var threshold = value;
      
      var thresholded_links = graph.links.filter(function(d){ return (d.value > threshold);});
      
      force
        .links(thresholded_links);

      var link = links_g.selectAll(".link")
        .data(thresholded_links, function(d){ return d.i; });

      link.enter().append("line")
        .attr("class", "link")
        .style("stroke-width", function(d) { return Math.sqrt(d.value); });

      link.exit().remove();

      force.on("tick", function() {
        link
          .attr("x1", function(d) { return d.source.x; })
          .attr("y1", function(d) { return d.source.y; })
          .attr("x2", function(d) { return d.target.x; })
          .attr("y2", function(d) { return d.target.y; });

        node
          .attr("cx", function(d) { return d.x; })
          .attr("cy", function(d) { return d.y; });
      });

      force.start();

    }

    force
      .nodes(graph.nodes);

    var node = nodes_g.selectAll(".node")
      .data(graph.nodes)
      .enter().append("circle")
        .attr("class", "node")
        .attr("r", 5)
        .style("fill", function(d) { return color(d.group); })
        .call(force.drag);

    node
      .append("title")
      .text(funtion(d) { return d.name; });

    brush.on("brush", brushed);

    slider
      .call(brush.extent([5, 5]))
      .call(brush.event);

  });
}

window.onload = function() {
  init_d3();
}