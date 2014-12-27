#!/usr/bin/env python
# coding=utf-8
import web
import sae.const
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

#数据库配置
db = web.database(dbn='mysql', user=sae.const.MYSQL_USER, pw=sae.const.MYSQL_PASS,
                  host=sae.const.MYSQL_HOST, port=int(sae.const.MYSQL_PORT), db=sae.const.MYSQL_DB)


