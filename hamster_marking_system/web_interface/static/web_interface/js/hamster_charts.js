//Bar graph for the frequency in statistics
function draw_frequency_graph(freq1, freq2, freq3, freq4, freq5) {
alert("Bar called!!");
    // Get the context of the canvas element we want to select
    var ctx = document.getElementById("frequency_bar_chart").getContext("2d");

    var bar_data_frequency = {
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

    var myBarChart = new Chart(ctx).Bar(bar_data_frequency, options);

}

function canYouSeeMe() {
    Alert("You can see me!!");
}

