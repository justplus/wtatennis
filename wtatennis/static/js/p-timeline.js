$(function(){
    $('#search_box').autocomplete({
        source:function(query,process){
            $.post("/timeline",{"keyword":query},function(respData){
                return process(respData);
            });
        },
        formatItem:function(item){
            return item["CH_NAME"]+"("+item["EN_NAME"]+") - "+item["COUNTRY"];
        },
        setValue:function(item){
            return {'data-value':item["CH_NAME"],'real-value':item["PLAYERID"]};
        }

    });

    $('#search-btn').click(function(){
        var player_id = $("#search_box").attr("real-value") || "";
        if(player_id){
            window.location.href="/timeline?player=" + player_id;
        }
    })
})