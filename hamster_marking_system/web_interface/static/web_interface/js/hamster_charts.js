//Bar graph for the frequency in statistics
function draw_frequency_graph(freq1, freq2, freq3, freq4, freq5) {
alert("Bar called!!");
    // Get the context of the canvas element we want to select
    var ctx = document.getElementById("frequency_bar_chart").getContext("2d");

    var data = {
        labels: ["0 - 39", "40 - 49", "50 - 59", "60 - 74", "75 - 100"],
        datasets: [
            {
                label: "Frequency of students",
                fillColor: "rgba(220,220,220,0.5)",
                strokeColor: "rgba(220,220,220,0.8)",
                highlightFill: "rgba(220,220,220,0.75)",
                highlightStroke: "rgba(220,220,220,1)",
                data: [freq1, freq2,freq3, freq4, freq5]
            }
        ]
    };
    
    var options = {

        ///Boolean - Whether grid lines are shown across the chart
        scaleShowGridLines : true,
    
        //String - Colour of the grid lines
        scaleGridLineColor : "rgba(0,0,0,.05)",
    
        //Number - Width of the grid lines
        scaleGridLineWidth : 1,
    
        //Boolean - Whether the line is curved between points
        bezierCurve : true,
    
        //Number - Tension of the bezier curve between points
        bezierCurveTension : 0.4,
    
        //Boolean - Whether to show a dot for each point
        pointDot : true,
    
        //Number - Radius of each point dot in pixels
        pointDotRadius : 4,
    
        //Number - Pixel width of point dot stroke
        pointDotStrokeWidth : 1,
    
        //Number - amount extra to add to the radius to cater for hit detection outside the drawn point
        pointHitDetectionRadius : 20,
    
        //Boolean - Whether to show a stroke for datasets
        datasetStroke : true,
    
        //Number - Pixel width of dataset stroke
        datasetStrokeWidth : 2,
    
        //Boolean - Whether to fill the dataset with a colour
        datasetFill : true,
    
        //String - A legend template
        legendTemplate : "<ul class=\"<%=name.toLowerCase()%>-legend\"><% for (var i=0; i<datasets.length; i++){%><li><span style=\"background-color:<%=datasets[i].lineColor%>\"></span><%if(datasets[i].label){%><%=datasets[i].label%><%}%></li><%}%></ul>"
    
    };


    var myBarChart = new Chart(ctx).Bar(data, options);

}

function canYouSeeMe() {
    Alert("You can see me!!");
}

