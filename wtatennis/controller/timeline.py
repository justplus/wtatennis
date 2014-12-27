#!/usr/bin/env python
# coding=utf-8
import json
from controller import setting
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

db = setting.db

def top_timeline_json(skip=0, limit=30):
    sql = 'select * from player p left join country c on p.country=c.country_enname where p.currentrank between $skip and $limit'
    results = db.query(sql, vars={'skip': skip, 'limit': limit})
    #'text': '<input type="text" id="search_box" style="width:250px;margin-left:350px;" placeholder="请输入球员姓名" autocomplete="off"></input><button type="submit"  class="btn search_btn" style="margin:-10px 0 0 20px;">搜索</button>',
    timeline = {
        'timeline': {
            'headline': ' ',
            'type': 'default',
            'startDate': '2014',
            'text': '',
            'asset':{
                'media': '',
                'credit': '',
                'caption': ''
            },
            'date': []
        }
    }
    for r in results:
        player_id = r.PLAYERID
        player_en_name = r.EN_NAME
        player_ch_name = r.CH_NAME
        birthday = r.BIRTHDAY
        photo = r.PHOTO
        points = r.POINTS
        champion_points = r.CHAMPIONPOINTS
        current_rank = r.CURRENTRANK
        champion_rank = r.CHAMPIONRANK
        high_rank = r.HIGHRANK
        high_rank_date = r.HIGHRANKDATE
        height = r.HEIGHT
        weight = r.WEIGHT
        single_titles = r.SINGLETITLES
        double_titles = r.DOUBLETITLES
        prize_money = r.PRIZEMONEY
        single_win = r.SINGLEWIN
        single_lose = r.SINGLELOSE
        double_win = r.DOUBLEWIN
        double_lose = r.DOUBLELOSE
        ytd_single_titles = r.YTDSINGLETITLES
        ytd_double_titles = r.YTDDOUBLETITLES
        ytd_prize_money = r.YTDPRIZEMONEY
        ytd_single_win = r.YTDSINGLEWIN
        ytd_single_lose = r.YTDSINGLELOSE
        ytd_double_win = r.YTDDOUBLEWIN
        ytd_double_lose = r.YTDDOUBLELOSE
        #country_abb = r.ABB
        country_ch_name = r.COUNTRY_CHNAME
        country_en_name = r.COUNTRY_ENNAME
        p_text = "<table class='playresults' style='width:300px;float:left'><tbody><tr><td><strong>国籍</strong></td>" \
                 "<td>%s</td></tr><tr><td><strong>生日</strong></td><td>%s</td></tr><tr><td>" \
                 "<strong>身高/体重</strong></td><td>%s/%s</td></tr><tr><td><strong>积分/排名</strong></td>" \
                 "<td>%s/%s</td></tr><tr><td><strong>冠军积分/排名</strong></td><td>%s/%s</td></tr><tr>" \
                 "<td><strong>最高排名</strong></td><td>%s(%s)</td></tr></tbody></table>" \
                 "<table class='playresults' style='position:absolute; left: 420px;'><thead><tr><td></td><td>今年</td>" \
                 "<td>职业生涯</td></tr></thead><tbody><tr><td><strong>WTA单打头衔</strong></td><td>%s</td>" \
                 "<td>%s</td></tr><tr><td><strong>WTA双打头衔</strong></td><td>%s</td><td>%s</td></tr>" \
                 "<tr><td><strong>比赛奖金</strong></td><td>$%s</td><td>$%s</td></tr><tr><td>" \
                 "<strong>单打胜负场数</strong></td><td>%s-%s</td><td>%s-%s</td></tr><tr><td>" \
                 "<strong>双打胜负场数</strong></td><td>%s-%s</td><td>%s-%s</td></tr></tbody></table>" \
            % (country_ch_name, birthday, height, weight, points, current_rank, champion_points, champion_rank,
                    high_rank, high_rank_date, ytd_single_titles, single_titles, ytd_double_titles, double_titles, ytd_prize_money,
                    prize_money, ytd_single_win, ytd_single_lose, single_win, single_lose, ytd_double_win, ytd_double_lose, double_win, double_lose)

        p_timeline = {
            'startDate': birthday.replace('.', ','),
            'headline': '%s%s' % (player_ch_name, '('+player_en_name+')' if player_ch_name != player_en_name else ''),
            'text': p_text,
            'asset':
            {
                'media': '',
                'credit': '',
                'caption': ''
            }
        }
        timeline['timeline']['date'].append(p_timeline)
    return json.dumps(timeline)

def player_timeline_json(player_id):
    sql = 'select * from player p left join country c on p.country=c.country_enname where p.playerid = $player_id'
    results = db.query(sql, vars={'player_id': player_id})
    timeline = {
        'timeline': {
            'headline': ' ',
            'type': 'default',
            'startDate': '2014',
            'text': '',
            'asset': {
                'media': '',
                'credit': '',
                'caption': ''
            },
            'date': []
        }
    }
    for r in results:
        player_id = r.PLAYERID
        player_en_name = r.EN_NAME if r.EN_NAME else 'BYE'
        player_ch_name = r.CH_NAME
        birthday = r.BIRTHDAY
        photo = r.PHOTO
        points = r.POINTS
        champion_points = r.CHAMPIONPOINTS
        current_rank = r.CURRENTRANK
        champion_rank = r.CHAMPIONRANK
        high_rank = r.HIGHRANK
        high_rank_date = r.HIGHRANKDATE
        height = r.HEIGHT
        weight = r.WEIGHT
        single_titles = r.SINGLETITLES
        double_titles = r.DOUBLETITLES
        prize_money = r.PRIZEMONEY
        single_win = r.SINGLEWIN
        single_lose = r.SINGLELOSE
        double_win = r.DOUBLEWIN
        double_lose = r.DOUBLELOSE
        ytd_single_titles = r.YTDSINGLETITLES
        ytd_double_titles = r.YTDDOUBLETITLES
        ytd_prize_money = r.YTDPRIZEMONEY
        ytd_single_win = r.YTDSINGLEWIN
        ytd_single_lose = r.YTDSINGLELOSE
        ytd_double_win = r.YTDDOUBLEWIN
        ytd_double_lose = r.YTDDOUBLELOSE
        country_ch_name = r.COUNTRY_CHNAME
        country_en_name = r.COUNTRY_ENNAME
        p_text = "<table class='playresults' style='width:300px;float:left'><tbody><tr><td><strong>国籍</strong></td>" \
                 "<td>%s</td></tr><tr><td><strong>生日</strong></td><td>%s</td></tr><tr><td>" \
                 "<strong>身高/体重</strong></td><td>%s/%s</td></tr><tr><td><strong>积分/排名</strong></td>" \
                 "<td>%s/%s</td></tr><tr><td><strong>冠军积分/排名</strong></td><td>%s/%s</td></tr><tr>" \
                 "<td><strong>最高排名</strong></td><td>%s(%s)</td></tr></tbody></table>" \
                 "<table class='playresults' style='position:absolute; left: 420px;'><thead><tr><td></td><td>今年</td>" \
                 "<td>职业生涯</td></tr></thead><tbody><tr><td><strong>WTA单打头衔</strong></td><td>%s</td>" \
                 "<td>%s</td></tr><tr><td><strong>WTA双打头衔</strong></td><td>%s</td><td>%s</td></tr>" \
                 "<tr><td><strong>比赛奖金</strong></td><td>$%s</td><td>$%s</td></tr><tr><td>" \
                 "<strong>单打胜负场数</strong></td><td>%s-%s</td><td>%s-%s</td></tr><tr><td>" \
                 "<strong>双打胜负场数</strong></td><td>%s-%s</td><td>%s-%s</td></tr></tbody></table>" \
            % (country_ch_name, birthday, height, weight, points, current_rank, champion_points, champion_rank,
                    high_rank, high_rank_date, ytd_single_titles, single_titles, ytd_double_titles, double_titles, ytd_prize_money,
                    prize_money, ytd_single_win, ytd_single_lose, single_win, single_lose, ytd_double_win, ytd_double_lose, double_win, double_lose)
        timeline['timeline']['headline'] = '%s%s' % (player_ch_name, '('+player_en_name.strip()+')' if player_ch_name != player_en_name else '')
        timeline['timeline']['text'] = p_text
        break
    sql = "select * from (select h.*, p.CH_NAME, p.EN_NAME from head2head h left join player p on h.player2=p.playerid where h.player1=$player_id) h1 left join tournament t on h1.tournamentid=t.id where t.tier in ('WTA','Grand Slam') order by h1.id asc"
    results = db.query(sql, vars={'player_id': player_id})

    t_results = {}
    for r in results:
        hold_date = r.HOLDDATE
        if not t_results.get(hold_date, None):
            t_results[hold_date] = []
        t_results[hold_date].append(r)
    dt_content = []
    for hold_dt, value in t_results.items():
        dt = {
            'headline': '',
            'startDate': '',
            'text': '',
            'asset': {
                'media': '',
                'credit': '',
                'caption': ''
            }
        }
        t_text = "<table class='playresults'><thead><tr><td>轮次</td><td>对手</td><td>比分</td><td>胜负</td><td>精彩片段</td></tr></thead><tbody>"
        for ind, v in enumerate(value):
            player2_id = v.PLAYER2
            h2h_id = v.ID
            hold_date = v.HOLDDATE.replace('.', ',')
            tournament_name = v.NAME if v.NAME and v.NAME != '-' else v.CITY
            player_rank = v.PLAYER1RANK if v.PLAYER1RANK != 0 else '-'
            player2_rank = v.PLAYER2RANK if v.PLAYER2RANK != 0 else '-'
            round = v.ROUND
            player2_ch_name = v.CH_NAME if v.CH_NAME else v.EN_NAME
            score = v.SCORE
            win = '√' if str(v.WINNER) == str(player_id) else '×'
            place = v.PHOTO if v.PHOTO else '默认'
            player2 = "<a href='/timeline?player=%s'>%s(%s)</a>" % (player2_id, player2_ch_name, player2_rank)
            pic_url = 'http://wtatennis-city.stor.sinaapp.com/%s.jpg' % place
            operation = '<a href="javascript:void(0);" onclick="viewhl(%s)">查看HL</a>' % h2h_id if v.HIGHLIGHT else '<a href="javascript:void(0);" onclick="addhl(%s)">添加HL</a>' % h2h_id
            if player2_id == 0:
                player2 = 'BYE'
                operation = ''
            t_text = t_text + "<tr><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td>" % (round, player2, score, win, operation)
            if ind == 0:
                dt['headline'] = '%s(%s)' % (tournament_name, player_rank)
                dt['asset']['media'] = pic_url
                dt['asset']['caption'] = place if place != '默认' else tournament_name
                dt['startDate'] = hold_date
        dt['text'] = t_text
        dt_content.append(dt)
    timeline['timeline']['date'] = dt_content
    return json.dumps(timeline)