$(function(){
    $('#search_box').autocomplete({
        source:function(query,process){
            sel_text = $("#search_type").find("option:selected").text();
            $.post("/data",{"keyword":query, "category": sel_text},function(respData){
                return process(respData);
            });
        },
        formatItem:function(item){
            if(sel_text == '球员'){
                return item["CH_NAME"]+"("+item["EN_NAME"]+") - "+item["COUNTRY"];
            }
            else if(sel_text == '赛事'){
                return item["PHOTO"]+"("+item["NAME"]+") - "+item["COUNTRY"];
            }
            else if(sel_text == '国家'){
                return item["COUNTRY_CHNAME"]+"("+item["COUNTRY_ENNAME"]+")";
            }
        },
        setValue:function(item){
            if(sel_text == '球员'){
                return {'data-value':item["CH_NAME"],'real-value':item["PLAYERID"]};
            }
            else if(sel_text == '赛事'){
                return {'data-value':item["NAME"],'real-value':item["TOURNAMENTID"]};
            }
            else if(sel_text == '国家'){
                return {'data-value':item["COUNTRY_CHNAME"],'real-value':item["COUNTRY_ENNAME"]};
            }
        }

    });

    $('#search-btn').click(function(){
        var pid = $("#search_box").attr("real-value") || "";
        if(sel_text == '球员'){
            window.location.href="/data?player=" + pid;
        }
        else if(sel_text == '赛事'){
            window.location.href="/data?tournament=" + pid;
        }
        else if(sel_text == '国家'){
            window.location.href="/data?country=" + pid;
        }
    })
})