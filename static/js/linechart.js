function LineChart (data, chart) {
	this.data = data;

	this.margin = chart.margin || { top: 0, bottom: 0, left: 0, right: 0 };
	this.height = chart.height || 100;
	this.width = chart.width || 400;
	this.target = chart.target || 'body';
	this.specialTextAppendage = chart.specialTextAppendage || 'ms';
	this.yLabelClass = chart.classes.yLabelClass || 'y-label';
	this.yTicksClass = chart.classes.yTicksClass || 'y-ticks';
	this.specialTextClass = chart.classes.specialTextClass || 'special-text';
		
	this.y = d3.scale.linear()
		.domain([0, d3.max(this.data)])
		.range([this.margin.bottom, this.height - this.margin.bottom]);
	
	this.x = d3.scale.linear()
		.domain([0, this.data.length])
		.range([this.margin.left, this.width - this.margin.left]);
	
	this.svg = d3.select(this.target)
		.append("svg:svg")
		.attr("width", this.width)
		.attr("height", this.height);

	this.g = this.svg.append("svg:g")
		.attr("transform", "translate(0, " + this.height + ")");

	this.line = d3.svg.line()
		.interpolate('linear')
		.x(function (d, i) { return this.x(i); })
		.y(function (d) { return -1 * this.y(d); });
}
LineChart.prototype = {
	draw: function () {
		var self = this;
		this.g.selectAll("." + this.yLabelClass)
			.data(this.y.ticks(2))
			.enter().append("svg:text")
			.attr("class", this.yLabelClass)
			.text(String)
			.attr("x", d3.select(this.target).attr('width') - 50)
			.attr("y", function(d) { return -1 * self.y(d) })
			.attr("text-anchor", "left")
			.attr("dy", 5);

		this.g.selectAll("." + this.yTicksClass)
			.data(this.y.ticks(2))
			.enter().append("svg:line")
			.attr("class", this.yTicksClass)
			.attr("y1", function(d) { return -1 * self.y(d); })
			.attr("x1", this.x(-0.3))
			.attr("y2", function(d) { return -1 * self.y(d); })
			.attr("x2", d3.select('svg').attr('width') - 70);

		this.g.append('text')
			.attr({
				class: self.specialTextClass,
				y: -2,
				x: 0
			})
			.text(this.data[this.data.length - 1] + self.specialTextAppendage);

		this.g.append("svg:path").attr("d", this.line(this.data));
	}
}
