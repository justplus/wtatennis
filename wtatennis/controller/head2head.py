#!/usr/bin/env python
# coding=utf-8
from controller import setting
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

db = setting.db

def player_info(player1_id, player2_id):
    player_info_sql = 'select * from player where playerid in ($player1_id, $player2_id)'
    results = db.query(player_info_sql, vars={'player1_id': player1_id, 'player2_id': player2_id})
    two_infos = []
    for r in results:
        two_infos.append(r)
    h2h_sql = 'select * from head2head h left join tournament t on h.tournamentid=t.id where h.player1=$player1_id and player2=$player2_id'
    results = db.query(h2h_sql, vars={'player1_id': player1_id, 'player2_id': player2_id})
    #<thead><tr><td>时间</td><td>赛事</td><td>轮次</td><td>胜者</td><td>比分</td><td>负者</td></tr></thead>
    h2h_info = """
    <table class="table"><thead style="font-weight:bolder; background:azure"><tr><td>时间</td><td>赛事</td><td>轮次</td><td>胜者</td><td>比分</td><td>负者</td></tr></thead>
        <tbody>"""
    player1_name = two_infos[0].CH_NAME
    player2_name = two_infos[1].CH_NAME
    player1_w_count = 0
    player2_w_count = 0
    for r in results:
        sur = r.SURFACE.lower()
        if sur[:4] == 'hard' or sur[:4] == 'clay':
            surface = sur[:4] + 'surface'
        elif sur[:5] == 'grass':
            surface = 'grasssurface'
        else:
            surface = 'nansurface'
        if r.WINNER == player1_id:
            player1_w_count += 1
            score = "<td>%s(%s)</td> <td>%s</td> <td>%s(%s)</td>" % (player1_name, r.PLAYER1RANK, r.SCORE, player2_name, r.PLAYER2RANK)
        else:
            player2_w_count += 1
            score = "<td>%s(%s)</td> <td>%s</td> <td>%s(%s)</td>" % (player2_name, r.PLAYER2RANK, r.SCORE, player1_name, r.PLAYER1RANK)
        h2h_info += '<tr class="%s"><td>%s</td><td>%s(%s)</td><td>%s</td>%s</tr>' % (surface, r.HOLDDATE, r.NAME, r.PHOTO, r.ROUND, score)
    h2h_info += '</tbody></table>'
    #<span style="font-size:5.5em;">%s-%s</span>
    #player1_w_count, player2_w_count,
    basic_info = """
    <span style="display:none;" id="player1_w">%s</span><span style="display:none;" id="player2_w">%s</span>
    <div class="h2h col-md-12" style="padding-left:0; padding-right:0">
        <table class="table table-striped table-bordered" style="margin-top:15px;">
            <tr>
            <td><a href="/timeline?player=%s"><img src="http://www.wtatennis.com/%s" width="150" height="200"></a></td>
            <td><img src="/static/images/h2h.png" width="194" height="50"><br/><span class="win1">%s</span><canvas id="canvas" height="150" width="150"></canvas><span class="win2">%s</span></td>
            <td><a href="/timeline?player=%s"><img src="http://www.wtatennis.com/%s" width="150" height="200"></a></td>
            </tr>
            <tr><td>%s</td><td>姓名</td><td>%s</td></tr>
            <tr><td>%s</td><td>生日</td><td>%s</td></tr>
            <tr><td>%s</td><td>身高</td><td>%s</td></tr>
            <tr><td>%s</td><td>体重</td><td>%s</td></tr>
            <tr><td>%s</td><td>52积分</td><td>%s</td></tr>
            <tr><td>%s</td><td>冠军积分</td><td>%s</td></tr>
            <tr><td>%s(%s)</td><td>最高排名(日期)</td><td>%s(%s)</td></tr>
            <tr><td>%s</td><td>本赛季单打头衔</td><td>%s</td></tr>
            <tr><td>$%s</td><td>本赛季奖金数</td><td>$%s</td></tr>
            <tr><td>%s/%s</td><td>本赛季胜负场</td><td>%s/%s</td></tr>
            <tr><td>%s</td><td>职业生涯单打头衔</td><td>%s</td></tr>
            <tr><td>$%s</td><td>职业生涯奖金数</td><td>$%s</td></tr>
            <tr><td>%s(%s)</td><td>职业生涯胜负场</td><td>%s(%s)</td></tr>
        </table>
    </div>
    <div class="col-md-12" style="padding-left:0; padding-right:0">
        %s
    </div>
    """ % (player1_w_count, player2_w_count, two_infos[0].PLAYERID, two_infos[0].PHOTO, player1_w_count, player2_w_count, two_infos[1].PLAYERID, two_infos[1].PHOTO, two_infos[0].CH_NAME,two_infos[1].CH_NAME,
    two_infos[0].BIRTHDAY, two_infos[1].BIRTHDAY, two_infos[0].HEIGHT,two_infos[1].HEIGHT,two_infos[0].WEIGHT,
    two_infos[1].WEIGHT, two_infos[0].POINTS,two_infos[1].POINTS, two_infos[0].CHAMPIONPOINTS,two_infos[1].CHAMPIONPOINTS,
    two_infos[0].HIGHRANK,two_infos[0].HIGHRANKDATE,two_infos[1].HIGHRANK, two_infos[1].HIGHRANKDATE,
    two_infos[0].YTDSINGLETITLES,two_infos[1].YTDSINGLETITLES, two_infos[0].YTDPRIZEMONEY,two_infos[1].YTDPRIZEMONEY,
    two_infos[0].YTDSINGLEWIN, two_infos[0].YTDSINGLELOSE,two_infos[1].YTDSINGLEWIN, two_infos[1].YTDSINGLELOSE,
    two_infos[0].SINGLETITLES,two_infos[1].SINGLETITLES, two_infos[0].PRIZEMONEY,two_infos[1].PRIZEMONEY,
    two_infos[0].SINGLEWIN, two_infos[0].SINGLELOSE,two_infos[1].SINGLEWIN, two_infos[1].SINGLELOSE, h2h_info)
    return basic_info