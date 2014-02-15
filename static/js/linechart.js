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
		.domain([
			d3.min(this.data, function (d) {
				return d.value;
			}),
			d3.max(this.data, function (d) {
				return d.value;
			})])
		.range([this.margin.bottom, this.height - this.margin.bottom]);
	
	this.x = d3.scale.linear()
		.domain([0, this.data.length])
		.range([this.margin.left, this.width - this.margin.left]);
	
	this.svg = d3.select(this.target)
		.append("svg:svg")
		.attr("width", this.width)
		.attr("height", this.height);

	this.meta = this.svg.append("svg:g")
		.attr({
			transform: "translate(0, " + this.height + ")",
			class: 'meta'
		});

	this.g = this.svg.append("svg:g")
		.attr({
			transform: "translate(0, " + this.height + ")",
			class: 'path'
		});

	this.line = d3.svg.line()
		.interpolate('linear')
		.x(function (d, i) { return this.x(i) - 40; })
		.y(function (d) { return -1 * this.y(d); });

	this.circle_group = this.svg.append("svg:g")
		.attr({
			transform: "translate(0, " + this.height + ")"
		});

	this.circles = this.circle_group.selectAll('circle').data(this.data);
}
LineChart.prototype = {
	draw: function () {
		var self = this;

		this.meta.selectAll("." + this.yLabelClass)
			.data(this.y.ticks(3))
			.enter().append("svg:text")
			.attr("class", this.yLabelClass)
			.text(String)
			.attr("x", $(self.target).parent().width() - 40)
			.attr("y", function(d) { return -1 * self.y(d) })
			.attr("text-anchor", "left")
			.attr("dy", 5);

		this.meta.selectAll("." + this.yTicksClass)
			.data(this.y.ticks(3	))
			.enter().append("svg:line")
			.attr("class", this.yTicksClass)
			.attr("y1", function (d) { return -1 * self.y(d); })
			.attr("x1", this.x(-0.3))
			.attr("y2", function (d) { return -1 * self.y(d); })
			.attr("x2", $(self.target).parent().width() - 45);

		this.meta.append('text')
			.attr({
				class: self.specialTextClass,
				y: -2,
				x: 0
			})
			.text(this.data[this.data.length - 1].value + self.specialTextAppendage);

		this.meta.append('text')
			.attr({
				class: 'time',
				y: function () {
					return -self.height + 20;
				},
				x: 0
			})
			.text('An hour ago');

		this.g.append("svg:path").attr("d", this.line(this.data));

		this.circles.enter()
			.append('circle')
			.attr({
				fill: 'rgba(200, 200, 200, 0)',
				cx: function (d, i) { return self.x(i) - 40; },
				cy: function (d) { return -1 * self.y(d); },
				r: 10
			})
			.on('mouseover', function (d) {
				d3.select(this)
					.transition()
					.attr('fill', 'rgba(200, 200, 200, .8)')
					.duration(500);

				self.meta.select('.' + self.specialTextClass)
					.text(d + self.specialTextAppendage);

				self.meta.select('.time')
					.text('stuff');
			})
			.on('mouseout', function (d) {
				d3.select(this)
					.transition()
					.attr('fill', 'rgba(200, 200, 200, 0)')
					.duration(500);

				self.meta.select('.' + self.specialTextClass)
					.text(self.data[self.data.length - 1].value + self.specialTextAppendage);

				self.meta.select('.time')
					.text(self.data[self.data.length - 1]);
			});
	}
}
