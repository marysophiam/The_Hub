function init_d3() {
  var width = 1280;
  var height = 580;

  var color = d3.scale.category10();

  var force = d3.layout.force()
    .charge(-400)
    .linkDistance(110)
    .size([width, height]);

  // domain is timeline; range is literal size of slider field  
  // the wider the range, the longer the value of one step on the slider
  var x = d3.scale.linear()
    .domain([16, 0])
    .range([540, 100])
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
  // somewhere in here is where to change color of numbers on slider???
  svg.append("g")
    .attr("class", "x axis")
    //move this to match slider handle & text
    // .attr("transform", "translate(" + (width - 20)  + ",0)")
    .attr("transform", "translate(" + 1080  + ",0)")
    .attr("fill", "white")
    .call(d3.svg.axis()
      .scale(x)
      .orient("left") // change this to "bottom" to display horizontally & adjust other things as necessary
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

  // slider handle
  // OOOH I WANT A MINI-TARDIS FOR THE SLIDER HANDLE!!!
  var handle = slider.append("circle")
    .attr("class", "handle")
    // move this to match slider & text
    // .attr("transform", "translate(" + (width - 20) + ",0)")
    .attr("transform", "translate(" + 1080 + ",0)")
    .attr("r", 5);

  svg.append("text")
    // x & y are location of text (above slider)
    .attr("x", 1080)
    .attr("y", 75)
    .attr("text-anchor", "end")
    .attr("font-size", "20px")
    // This changes .text color, but not numbers next to slider
    .attr("fill", "white")
    .style("opacity", 0.5)
    .text("Timeline")

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
      
      // threshold now <= value (instead of >); means timeline is start to end
      var thresholded_links = graph.links.filter(function(d){ return (d.value <= threshold);});
      
      force
        .links(thresholded_links);

      var link = links_g.selectAll(".link")
        .data(thresholded_links, function(d){ return d.i; });

      link.enter().append("line")
        .attr("class", "link")
        .style("stroke-width", 3);
        // If stroke width uses this function, links will be thicker the older the connection
        // .style("stroke-width", function(d) { return Math.sqrt(d.value); });

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
        .attr("r", 8)
        .style("fill", function(d) { return color(d.group); })
        .call(force.drag);

    node
      .append("title")
      .text(function(d) { return d.name; });

    brush.on("brush", brushed);

    slider
      .call(brush.extent([0, 0]))
      .call(brush.event);

  });
}

function setupCarousel(carouselName) {
  var carousel = new MultiCarousel({
    target: document.getElementById(carouselName),
    data: {
      delay: 2000,
      items: Array.prototype.slice.call(document.getElementById(carouselName).children),
      count: 5
    }
  });
      document.getElementById(carouselName).style.display = "block";
      // document.getElementById(carouselName + ".previous").onclick = function() {carousel.previous()}

      // document.getElementById(carouselName + ".pause").onclick = function() {carousel.pause()}

      // document.getElementById(carouselName + ".start").onclick = function() {carousel.start()}

      // document.getElementById(carouselName + ".next").onclick = function() {carousel.next()}
  }