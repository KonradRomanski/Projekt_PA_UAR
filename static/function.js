var interval = setInterval(update_values, 1000);
var c = 0;
var temp = 0;

function removeData(chart) {
  chart.data.labels.splice(0, 1);
  chart.data.datasets.forEach((dataset) => {
  dataset.data.splice(0, 1);
});
chart.update();
}

function update_values() {
  $SCRIPT_ROOT = {{ request.script_root|tojson|safe }};
  $.getJSON($SCRIPT_ROOT + '/_stuff',

  function(data){
    $("#result").text(data.result);
    temp = data.result;
    console.log(data);
  });

  c=c+1;
  console.log(c);
  console.log(temp);
  myChart.data.labels.push(c);
  myChart.data.datasets.forEach((dataset) => {
    dataset.data.push(temp);
  });
  myChart.update();
  if (c >20) removeData(myChart);
}
