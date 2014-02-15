function generateSimpleData (min, max, length) {
	var result = [];
	for (var i = 0; i < length; i++) {
		result.push(Math.floor(Math.random() * max) + min);
	}
	return result;
}

function generateTimeSeriesData (min, max, start, end, interval, interval_type) {
	var result = [],
		previous = start;
	while (previous <= end) {
		var time = moment(previous).add(interval_type, interval),
			object = {
				time: time.unix(),
				value: Math.floor(Math.random() * max) + min
			};
		result.push(object);
		previous = time;
	}
	return result;
}
