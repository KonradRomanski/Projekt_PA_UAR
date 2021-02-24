var ctx = document.getElementById('myChart').getContext('2d');
var myChart = new Chart(ctx, {
    type: 'line',
    data: {
        labels: [],
        datasets: [{
            label: 'temperatura',
            data: [],
            backgroundColor: [
                'rgba(54, 162, 235, 0.2)',
            ],
            borderColor: [
                'rgba(54, 162, 235, 1)',
            ],
            borderWidth: 1
        }]
    },
    options: {
      legend:{
        display: false
      },
      tooltips: {
    callbacks: {
       label: function(tooltipItem) {
              return tooltipItem.yLabel;
       }
    }
},
      responsive: true,
      maintainAspectRatio: true,
      animation:{
        easing: 'easeOutElastic'
      },
        scales: {
            yAxes: [{
              scaleLabel: {
                display: true,
                labelString: 'Temperatura [K]'
              },
              gridLines: {
                display: false,
                drawOnChartArea: false
              },
              display: true,
                ticks: {
                    beginAtZero: true
                    // min: 0,
                    // max: 10
                }
            }],
            xAxes: [{
              scaleLabel: {
                display: true,
                labelString: 'Czas [s]'
              },
    gridLines: {
        display: false,
        drawOnChartArea: false
    }
}]
        },
        elements: {
                   point:{
                       radius: 0
                   }
               }
    }
});
