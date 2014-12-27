#!/usr/bin/env python
# coding=utf-8
from controller import setting
import sae.storage
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

#数据库配置
db = setting.db

def retrieve(keyword, category):
    if category == '球员':
        sql = "select PLAYERID, CH_NAME, EN_NAME, COUNTRY from player where lower(concat(ch_name,'|',en_name)) " \
          "like '%" + keyword + "%' order by points desc limit 0,5"
    elif category == '赛事':
        sql = "select TOURNAMENTID, NAME, COUNTRY, PHOTO from (select *, count(distinct tournamentid) from tournament " \
              "group by tournamentid) tmp where lower(concat(photo,'|',name)) like '%" + keyword + "%' and name!='-' " \
               "order by prizemoney desc limit 0,5"
    elif category == '国家':
        sql = "select * from country where lower(concat(country_chname,'|',country_enname)) like '%" + keyword + "%' limit 0,5"
    results = db.query(sql)
    return list(results)

def get_country_highrank(country):
    sql = "select distinct PLAYER1, count(PLAYER1) as CNT, min(PLAYER1RANK) as RANK, YEAR from (select h.PLAYER1,h.PLAYER1RANK,substr(t.HOLDDATE,1, 4) as YEAR " \
          "from `head2head` h left join player p on h.PLAYER1=p.PLAYERID left join tournament t on h.TOURNAMENTID=t.ID " \
          "where p.COUNTRY=$country and PLAYER1RANK!=0 ORDER by YEAR) tmp GROUP BY YEAR"
    results = db.query(sql, locals())
    xlabels = []
    ylabels = []
    ylabels1 = []
    for result in results:
        xlabels.append(int(result['YEAR']))
        ylabels.append(int(result['RANK']))
        ylabels1.append(int(result['CNT']))
    return [xlabels, ylabels, ylabels1]

def get_country_topcount(country, n=100):
    sql = "select count(DISTINCT player1) as CNT, YEAR from (SELECT h.PLAYER1,h.PLAYER1RANK,substr(t.HOLDDATE,1, 4) as YEAR " \
          "FROM `head2head` h LEFT JOIN player p on h.PLAYER1=p.PLAYERID left join tournament t on h.TOURNAMENTID=t.ID " \
          "where p.COUNTRY=$country and PLAYER1RANK!=0 ORDER by YEAR) tmp where PLAYER1RANK<=$n GROUP BY YEAR "
    results = db.query(sql, locals())
    xlabels = []
    ylabels = []
    for result in results:
        xlabels.append(int(result['YEAR']))
        ylabels.append(int(result['CNT']))
    return [xlabels, ylabels]

def get_country_info(country):
    sql = "select ABB from country where COUNTRY_ENNAME=$country"
    result = db.query(sql, locals())
    tmp = list(result)
    abb = tmp[0]['ABB'] if len(tmp) > 0 else None
    #历史赛事数量
    sql = "SELECT count(distinct TOURNAMENTID) as CNT FROM `tournament` where country=$country and TIER='WTA'"
    results = db.query(sql, locals())
    tmp = list(results)
    tournament_count = tmp[0]['CNT'] if len(tmp) > 0 else 0
    #当前赛事数量和名称
    sql = "SELECT DISTINCT TOURNAMENTID,NAME FROM `tournament` where country=$country and TIER='WTA' and NAME!='-'"
    results = db.query(sql, locals())
    tournaments = {}
    for result in results:
        tournaments[result["TOURNAMENTID"]] = result['NAME']
    ytd_tournament_count = len(tournaments)
    #历史职业球员数量
    sql = "SELECT count(1) as CNT FROM `player` where country=$country"
    results = db.query(sql, locals())
    player_count = list(results)[0]['CNT']
    #当前职业球员数量
    sql = "SELECT count(1) as CNT FROM `player` where country=$country and POINTS>0"
    results = db.query(sql, locals())
    ytd_player_count = list(results)[0]['CNT']
    #历史最高排名球员
    sql = "SELECT * FROM `player` where country=$country and HIGHRANK!=-1 ORDER BY HIGHRANK asc,POINTS desc limit 0,6"
    results = db.query(sql, locals())
    highrank_players = []
    for result in results:
        highrank_players.append(result)
    return [tournament_count, ytd_tournament_count, player_count, ytd_player_count, tournaments, highrank_players, abb]

def get_tournament_info(tournament_id):
    sql = "select * from tournament where tournamentid=$tournament_id order by holddate asc"
    results = db.query(sql, locals())
    #举办次数
    years = 0
    photo = None
    year_list = []
    year_prize = []
    for result in results:
        photo = result['PHOTO']
        years += 1
        if result['PRIZEMONEY']:
            year_list.append(int(result['HOLDDATE'][:4]))
            year_prize.append(int(result['PRIZEMONEY']))
    sql = "select count(distinct winner) as CNT from previouswinner where tournamentid=$tournament_id"
    results = db.query(sql, locals())
    #冠军数量
    tmp = list(results)
    champions_count = tmp[0]['CNT'] if tmp else 0
    #冠军来自国家数量
    sql = "select count(distinct country) as CNT from player where en_name in (select distinct winner from previouswinner " \
          "where tournamentid=$tournament_id)"
    results = db.query(sql, locals())
    tmp = list(results)
    cham_country_count = tmp[0]['CNT'] if tmp else 0
    #获取冠军次数最多的球员
    sql = "select WINNER, count(1) as CNT from previouswinner where tournamentid=$tournament_id group by winner order by CNT desc"
    results = db.query(sql, locals())
    tmp = list(results)
    max_champ_count = tmp[0]['CNT'] if tmp else 0
    player = tmp[0]['WINNER'] if tmp else None
    #球员代表
    sql = "select * from (SELECT WINNER, count(1) as cnt FROM previouswinner where TOURNAMENTID=$tournament_id " \
          "GROUP BY WINNER ORDER BY cnt desc limit 0,6) tmp left join player p on p.EN_NAME=tmp.WINNER"
    results = db.query(sql, locals())
    highrank_players = []
    for result in results:
        highrank_players.append(result)
    #历届冠军
    sql = "select * from(select * from(select YEAR, WINNER from previouswinner where TOURNAMENTID=$tournament_id order by year desc) tmp" \
          " left join player p on p.EN_NAME=tmp.WINNER) tp left join country c on tp.country=c.COUNTRY_ENNAME"
    results = db.query(sql, locals())
    champions = []
    for result in results:
        champions.append(result)
    return [years, champions_count, max_champ_count, player, cham_country_count, photo, highrank_players, year_list, year_prize, champions]





