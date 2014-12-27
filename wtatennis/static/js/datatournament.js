$(function(){
    max = function(list){
        var max = list[0];
         var len = list.length;
         for (var i = 1; i < len; i++){
            if (list[i] > max) {
                max = list[i];
            }
         }
         return max;
	}

    var drawline = function(chart_x, chart_y, canvas_name){
        var lineChartData = {
			labels : JSON.parse(chart_x),
			datasets : [
				{
					fillColor : "rgba(151,187,205,0.5)",
					strokeColor : "rgba(151,187,205,1)",
					pointColor : "rgba(151,187,205,1)",
					pointStrokeColor : "#fff",
					data : JSON.parse(chart_y)
				}
			]
		}
	    var steps = 10;
        var max_val = max(JSON.parse(chart_y));
        var option = {scaleOverride: true, scaleSteps: steps, scaleStartValue: 0, 	scaleStepWidth: Math.ceil(max_val / steps)};
        var myLine = new Chart(document.getElementById(canvas_name).getContext("2d")).Line(lineChartData, option);
    }
    var chart1_x = $("#chart1_x").text();
    var chart1_y = $("#chart1_y").text();
    drawline(chart1_x, chart1_y, "canvas");
})