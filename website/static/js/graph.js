let temperature = [0,0,0,0,0,0,0,0,0,0];
let power = [0,0,0,0,0,0,0,0,0,0];

function get_response() {
	var data;
	$.ajax({
		url: '/live_temp',
		type: 'GET',
		datatype: 'json',
		async: false,
		success: function(response) {
			data = response;
		},
		fail: function(error) {
			console.log('Error ', error);
		}
		});
	return data;
};

function update_temp() {
	respond = get_response();
	// Update the latest value of temperature array
	temperature.shift()
	temperature.push(respond.temp);
	// Update the power usage with %
	$('#power-usage').empty();
	$('#power-usage').append("Usage "+respond.power+"%");
};

const ctx = document.getElementById('chart');

var chart = new Chart(ctx, {
	type: 'line',
	data: {
	labels: [0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
	datasets: [{
		data: temperature,
		label: 'Real time temperature',
		fill: false,
		borderWidth: 1
		}]
	},
	options: {
		scales: {
		xAxes: [{
			ticks: {
				min: 0,
				max: 10
			}
		}],
		yAxes: [{
			ticks: {
				min: 20,
				max: 50
			}
		}]
	}
  }
});

const doughnut_ctx = document.getElementById('power-chart');
var pie_chart = new Chart(doughnut_ctx, {
	type: 'doughnut',
	data: {
	labels: [
		0, 'Power Usage',
	],
	datasets: [{
		label: 'My First Dataset',
		data: [0,100],
		backgroundColor: [
			'rgb(255, 99, 132)',
			'rgb(54, 162, 235)'
		],
		hoverOffset: 4
	}]},
	options: {
		animation: {
		animateRotate: false,
		},
		tooltips: {enabled: false},
		hover: {mode: null},
  }
});

const usage_ctx = document.getElementById('power-usage-line');
var usage_chart = new Chart(usage_ctx, {
	type: 'line',
	data: {
	labels: [0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
	datasets: [{
		data: power,
		label: 'Real time Power Usage',
		fill: false,
		borderWidth: 1
		}]
	},
	options: {
		legend: {
		display: false
		},
		tooltips: {
			enabled: false
		},
		scales: {
		xAxes: [{
			ticks: {
				min: 0,
				max: 10
			}
		}],
		yAxes: [{
			ticks: {
				min: 0,
				max: 100
			}
		}]
	}
  }
});


function update_chart() {
	_data = get_response()
	if (typeof _data !== "undefined") {
		chart.data.datasets.forEach((dataset) => {
			dataset.data.shift()
		});
		chart.data.datasets.forEach((dataset) => {
			dataset.data.push(_data.temp);
		});
	}
	if (typeof _data !== "undefined") {
		usage_chart.data.datasets.forEach((dataset) => {
			dataset.data.shift()
		});
		usage_chart.data.datasets.forEach((dataset) => {
			dataset.data.push(_data.power);
		});
	}
	pie_chart.data.datasets.forEach((dataset) => {
		dataset.data.shift();
		dataset.data.shift()
	});
	pie_chart.data.datasets.forEach((dataset) => {
		dataset.data.push(100-_data.power);
		dataset.data.push(_data.power);
	});

	chart.update();
	pie_chart.update();
	usage_chart.update();
};

$(document).ready(function() {
	var updateInterval = 1000;
	update_temp();
	setInterval(update_temp, updateInterval);  // Update every 1 seconds
	setInterval(update_chart, updateInterval);  // Update every 1 seconds
});