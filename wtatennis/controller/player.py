#!/usr/bin/env python
# coding=utf-8
from controller import setting
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

db = setting.db

def top_players(order='championrank', skip=0, limit=8):
    sql = "select * from player where currentrank>0 order by %s asc limit %s, %s" % (order, skip, limit)
    results = db.query(sql)
    players = []
    for r in results:
        players.append(r)
    return players


