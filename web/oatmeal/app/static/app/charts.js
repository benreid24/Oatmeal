function drawTempGauge(name, temp) {
  var data = google.visualization.arrayToDataTable(
      [['Label', 'Value'], ['Temp', temp]]);
  var options = {
    width: '100%',
    height: 300,
    greenFrom: 70,
    greenTo: 83,
    redFrom: 83,
    redTo: 90,
    yellowFrom: 60,
    yellowTo: 70,
    min: 60,
    max: 90,
    majorTicks: ['60°', '65°', '70°', '75°', '80°', '85°', '90°'],
    minorTicks: 5,
    yellowColor: '#037ffc'
  };
  var formatter = new google.visualization.NumberFormat({'suffix': '°F'});
  formatter.format(data, 1);
  var chart =
      new google.visualization.Gauge(document.getElementById(name + '-tgauge'));
  chart.draw(data, options);
}

function drawHumidGauge(name, humid) {
  var data = google.visualization.arrayToDataTable(
      [['Label', 'Value'], ['RH', humid]]);
  var options = {
    width: '100%',
    height: 300,
    greenFrom: 60,
    greenTo: 100,
    redFrom: 20,
    redTo: 50,
    yellowFrom: 50,
    yellowTo: 60,
    min: 20,
    max: 100,
    majorTicks:
        ['20%', '30%', '40%', '50%', '60%', '70%', '80%', '90%', '100%'],
    minorTicks: 5
  };
  var formatter = new google.visualization.NumberFormat({'suffix': '%'});
  formatter.format(data, 1);
  var chart =
      new google.visualization.Gauge(document.getElementById(name + '-hgauge'));
  chart.draw(data, options);
}

function drawZoneLine(name, datapoints) {
  var data = new google.visualization.DataTable();
  data.addColumn('datetime', 'Time');
  data.addColumn('number', 'Temperature');
  data.addColumn('number', 'Humidity');
  data.addRows(datapoints);
  var options = {
    titlePosition: 'none',
    legend: {position: 'in', textStyle: {color: 'white', fontSize: 14}},
    width: '100%',
    height: 330,
    backgroundColor: 'transparent',
    chartArea: {
      backgroundColor: '#333333',
    },
    colors: ['#ff5555', '#7777ff'],
    curveType: 'function',
    series: {0: {targetAxisIndex: 0}, 1: {targetAxisIndex: 1}},
    vAxes: {
      0: {
        title: 'Temperature',
        titleTextStyle: {color: '#ff5555', fontSize: 18},
        viewWindow: {min: 60, max: 87},
        gridlines: {color: 'transparent'},
        textStyle: {color: 'white'},
        format: '##°F'
      },
      1: {
        title: 'Humidity',
        titleTextStyle: {color: '#7777ff', fontSize: 18},
        viewWindow: {min: 20, max: 102},
        gridlines: {color: 'transparent'},
        textStyle: {color: 'white'},
        format: '##\'%\''
      }
    },
    hAxis: {
      title: 'Time',
      titleTextStyle: {color: 'white', fontSize: 18},
      gridlines: {color: 'transparent'},
      textStyle: {color: 'white', fontSize: 14},
      format: 'HH:mm'
    }
  };

  var div = document.getElementById(name + '-tline');
  var chart = new google.visualization.LineChart(div);

  chart.draw(data, options);
}

function drawMotionLine(datapoints) {
  var data = new google.visualization.DataTable();
  data.addColumn('datetime', 'Time');
  data.addColumn('number', 'Motion');
  data.addRows(datapoints);
  var options = {
    titlePosition: 'none',
    legend: {position: 'none'},
    width: '100%',
    height: 330,
    backgroundColor: 'transparent',
    chartArea: {
      backgroundColor: '#333333',
    },
    colors: ['#33ff33'],
    curveType: 'function',
    vAxes: {
      0: {
        gridlines: {color: 'transparent'},
        textStyle: {color: 'transparent'},
      }
    },
    hAxis: {
      title: 'Time',
      titleTextStyle: {color: 'white', fontSize: 18},
      gridlines: {color: 'transparent'},
      textStyle: {color: 'white', fontSize: 14},
      format: 'HH:mm'
    }
  };

  var div = document.getElementById('motion_div');
  var chart = new google.visualization.LineChart(div);

  chart.draw(data, options);
}