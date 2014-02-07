var rgb = [
	'rgba(250, 250, 250, 0.5)',
	'rgba(250, 250, 250, 0.5)',
	'rgba(240, 240, 240, 0.5)',
	'rgba(240, 240, 240, 0.5)',
	'rgba(230, 230, 230, 0.5)',
	'rgba(230, 230, 230, 0.5)',
	'rgba(220, 220, 220, 0.5)',
	'rgba(220, 220, 220, 0.5)',
	'rgba(210, 210, 210, 0.5)',
	'rgba(210, 210, 210, 0.5)',
	'rgba(200, 200, 200, 0.5)',
	'rgba(200, 200, 200, 0.5)',
	'rgba(190, 190, 190, 0.5)',
	'rgba(190, 190, 190, 0.5)',
	'rgba(180, 180, 180, 0.5)',
	'rgba(180, 180, 180, 0.5)',
	'rgba(170, 170, 170, 0.5)',
	'rgba(170, 170, 170, 0.5)',
	'rgba(160, 160, 160, 0.5)',
	'rgba(160, 160, 160, 0.5)',
	'rgba(150, 150, 150, 0.5)',
	'rgba(150, 150, 150, 0.5)',
	'rgba(140, 140, 140, 0.5)',
	'rgba(140, 140, 140, 0.5)',
	'rgba(130, 130, 130, 0.5)',
	'rgba(130, 130, 130, 0.5)',
	'rgba(120, 120, 120, 0.5)',
	'rgba(120, 120, 120, 0.5)',
	'rgba(110, 110, 110, 0.5)',
	'rgba(110, 110, 110, 0.5)',
	'rgba(100, 100, 100, 0.5)',
	'rgba(100, 100, 100, 0.5)',
	'rgba(90, 90, 90, 0.5)',
	'rgba(90, 90, 90, 0.5)',
	'rgba(80, 80, 80, 0.5)',
	'rgba(80, 80, 80, 0.5)',
	'rgba(70, 70, 70, 0.5)',
	'rgba(70, 70, 70, 0.5)',
	'rgba(60, 60, 60, 0.5)',
	'rgba(60, 60, 60, 0.5)',
	'rgba(50, 50, 50, 0.5)',
	'rgba(50, 50, 50, 0.5)',
	'rgba(40, 40, 40, 0.5)',
	'rgba(40, 40, 40, 0.5)',
	'rgba(30, 30, 30, 0.5)',
	'rgba(30, 30, 30, 0.5)',
	'rgba(20, 20, 20, 0.5)',
	'rgba(20, 20, 20, 0.5)'
];
/**
* A bar chart. Required data format:
* [ { name : x-axis-bar-label, value : N }, ...]
*
*  Sample use:
*  var bargraph = d3.select('#bargraph')
*    .append('svg')
*    .attr('width', line_w)
*    .attr('height', line_h)
*    .chart('CC-Barchart')
*    .max(1.0);
*  bargraph.draw(bardata);
*/
d3.chart('BarChart', {
	initialize: function() {
		var chart = this;

		// default height and width
		chart.w = chart.base.attr('width') || 200;
		chart.h = chart.base.attr('height') || 150;

		// chart margins to account for labels.
		// we may want to have setters for this
		// if we were letting the users customize this too
		chart.margins = {
			top : 0,
			bottom : 0,
			left : 0,
			right : 0,
			padding : 2
		};

		// default chart ranges
		chart.x =  d3.scale.linear()
			.range([0, chart.w - chart.margins.left]);

		chart.y = d3.scale.linear()
			.range([chart.h - chart.margins.bottom, 0]);

		chart.base
			.classed('Barchart', true);

		// non data driven areas (as in not to be independatly drawn)
		chart.areas = {};

		chart.areas.bars = chart.base.append('g')
			.classed('bars', true)
			.attr('width', chart.w - chart.margins.left)
			.attr('height', chart.h - chart.margins.bottom - chart.margins.top);

		// make actual layers
		chart.layer('bars', chart.areas.bars, {
			// data format:
			// [ { name : x-axis-bar-label, value : N }, ...]
			dataBind : function(data) {

				// save the data in case we need to reset it
				chart.data = data;

				// how many bars?
				chart.bars = data.length;

				// compute box size
				chart.bar_width = (chart.w - chart.margins.left - ((chart.bars - 1) * chart.margins.padding)) / chart.bars;

				// adjust the x domain - the number of bars.
				chart.x.domain([0, chart.bars]);

				// adjust the y domain - find the max in the data.
				chart.datamax = chart.usermax || d3.max(data, function(d) { 
					return d; 
				});
				chart.y.domain([0, chart.datamax]);

				return this.selectAll('rect')
					.data(data);
			},
			insert : function() {
				return this.append('rect')
					.classed('bar', true)
					.attr('fill', function (d, i) { return rgb[i]; });
			}
		});

		// on new/update data
		// render the bars.
		var onEnter = function() {
			this.attr('x', function(d, i) {
						return chart.x(i) - 0.5;
					})
					.attr('y', function(d) {
						return chart.h - chart.margins.bottom - chart.margins.top - chart.y(chart.datamax - d) - 0.5;
					})
					.attr('val', function(d) {
						return d;
					})
					.attr('width', chart.bar_width)
					.attr('height', function(d) {
						//return chart.h - chart.margins.bottom - chart.y(chart.datamax - d);
						return chart.y(chart.datamax - d);
					})
					.transition().duration(1000);
		};

		chart.layer('bars').on('enter', onEnter);
		chart.layer('bars').on('update', onEnter);
	},

	// return or set the max of the data. otherwise
	// it will use the data max.
	max : function(datamax) {
		if (!arguments.length) {
			return this.usermax;
		}

		this.usermax = datamax;

		this.draw(this.data);

		return this;
	},

	width : function(newWidth) {
		if (!arguments.length) {
			return this.w;
		}
		// save new width
		this.w = newWidth;

		// adjust the x scale range
		this.x =  d3.scale.linear()
			.range([this.margins.left, this.w - this.margins.right]);

		// adjust the base width
		this.base.attr('width', this.w);

		this.draw(this.data);

		return this;
	},

	height : function(newHeight) {
		if (!arguments.length) {
			return this.h;
		}

		// save new height
		this.h = newHeight;

		// adjust the y scale
		this.y = d3.scale.linear()
			.range([this.h - this.margins.top, this.margins.bottom]);

		// adjust the base width
		this.base.attr('height', this.h);

		this.draw(this.data);
		return this;
	}
});
