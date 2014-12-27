#!/usr/bin/env python
# coding=utf-8
import re
import hashlib
import uuid
from controller import setting
import sae.storage
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

#数据库配置
db = setting.db

def check_nickname(nick_name):
    if not nick_name:
        return {'status': -1, 'message': u'昵称不能为空'}
    nick_name = nick_name.strip()
    if len(nick_name) < 4 or len(nick_name) > 10:
        return {'status': -1, 'message': u'昵称长度需在4到10之间'}
    else:
        sql = "select id from user where NICKNAME=$field"
        results = db.query(sql, vars={'field': nick_name})
        for r in results:
            return {'status': -1, 'message': u'昵称已被使用'}
        return {'status': 1}

def check_password(password):
    r = re.match(r'^(\w){6,20}$', password)
    if not r:
        return {'status': -1, 'message': u'密码长度需在6到20之间'}
    else:
        return {'status': 1}

def check_email(email):
    reg = r'^([a-zA-Z0-9]+[_|\_|\.]?)*[a-zA-Z0-9]+@([a-zA-Z0-9]+[_|\_|\.]?)*[a-zA-Z0-9]+\.[a-zA-Z]{2,3}$'
    r = re.match(reg, email)
    if not r:
        return {'status': -1, 'message': u'邮箱格式不符合要求'}
    else:
        sql = "select id from user where EMAIL=$field"
        results = db.query(sql, vars={'field': email})
        for r in results:
            if r:
                return {'status': -1, 'message': u'昵称已被使用'}
        return {'status': 1}

def add_user(username, password, email):
    encrypt_pwd = hashlib.new('md5', password).hexdigest()
    sql = 'insert into user (EMAIL, PASSWORD, NICKNAME) values ($email, $password, $username)'
    result = db.query(sql, {'email': email, 'password': encrypt_pwd, 'username': username})
    return True if result > 0 else False

def check_login(email, password):
    encrypt_pwd = hashlib.new('md5', password).hexdigest()
    sql = 'select * from user where email=$email and password=$password'
    results = db.query(sql, {'email': email, 'password': encrypt_pwd})
    for r in results:
        if r:
            return r
    return False

def get_areas(level=2, province_name=None):
    if level == 2:
        sql = 'select * from area where parentid=0'
        results = db.query(sql)
    elif level == 3:
        sql = 'select * from area where parentid = (select id from area where name=$name)'
        results = db.query(sql, vars={'name': province_name})
    else:
        results = None
    areas = []
    for r in results:
        areas.append(r.NAME)
    return areas

def upload_photo(file_bytes, ext):
    storage = sae.storage.Client()
    ob = sae.storage.Object(file_bytes)
    file_url = storage.put('photo', '%s%s' % (str(uuid.uuid1()), ext), ob)
    return file_url

def get_province_by_city(city_name):
    sql = 'select * from area where id=(select parentid from area where name=$city_name)'
    results = db.query(sql, vars={'city_name': city_name})
    return list(results)[0].NAME

def update_user(city_name, photo_url, introduce):
    sql = 'update user set city=$city_name, photo=$photo_url, introduce=$introduce'
    results = db.query(sql, locals())
    return results

def retrieve_user(keyword):
    sql = "select PLAYERID, CH_NAME, EN_NAME, COUNTRY from player where lower(concat(ch_name,'|',en_name)) " \
          "like '%" + keyword + "%' order by points desc limit 0,5"
    results = db.query(sql)
    return list(results)