var data = [432, 123, 432,123 ,765,234,234,656,800,123,431,543,652],
	w = 800,
	h = 100,
	margin = 10,
	y = d3.scale.linear()
		.domain([0, d3.max(data)])
		.range([0 + margin, h - margin]),
	x = d3.scale.linear()
		.domain([0, data.length])
		.range([0 + margin, w - margin]);

var vis = d3.select("body")
	.append("svg:svg")
	.attr("width", w)
	.attr("height", h);

var g = vis.append("svg:g")
	.attr("transform", "translate(0, " + h + ")");

var line = d3.svg.line()
	.interpolate('linear')
	.x(function(d,i) { return x(i); })
	.y(function(d) { return -1 * y(d); });


g.selectAll(".yLabel")
	.data(y.ticks(2))
	.enter().append("svg:text")
	.attr("class", "yLabel")
	.text(String)
	.attr("x", d3.select('svg').attr('width') - 50)
	.attr("y", function(d) { return -1 * y(d) })
	.attr("text-anchor", "left")
	.attr("dy", 5);

g.selectAll(".yTicks")
	.data(y.ticks(2))
	.enter().append("svg:line")
	.attr("class", "yTicks")
	.attr("y1", function(d) { return -1 * y(d); })
	.attr("x1", x(-0.3))
	.attr("y2", function(d) { return -1 * y(d); })
	.attr("x2", d3.select('svg').attr('width') - 70);
	//x(0));

g.append('text')
	.attr({
		class: 'special-text',
		y: -50,
		x: 0
	})
	.text(data[data.length - 1] + 'ms');

g.append("svg:path").attr("d", line(data));
