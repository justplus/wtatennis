$(function() {
    var player1_w = parseInt($("#player1_w").text());
    var player2_w = parseInt($("#player2_w").text());
    var pieData = [{value: player2_w/(player1_w+player2_w)*100, color: "#F38630"}, {value: player1_w/(player1_w+player2_w)*100, color: "#69D2E7"}];
    var myPie = new Chart(document.getElementById("canvas").getContext("2d")).Pie(pieData);
    //scroll the live-box
    var scrtime;
    $("#con").hover(function(){
         clearInterval(scrtime);
    },function(){
        scrtime = setInterval(function(){
            	var ul = $("#con ul");
                var liHeight = ul.find("li:last").height();
                ul.animate({marginTop : liHeight+40 +"px"},1000,function(){
                	ul.find("li:last").prependTo(ul)
                	//ul.find("li:first").hide();
                	ul.css({marginTop:0});
                	ul.find("li:first").fadeIn(1000);
                });
        },3000);
     }).trigger("mouseleave");
	$(".face img").corner("5px");
})