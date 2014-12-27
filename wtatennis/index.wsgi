#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import sae
import web
import json
import pylibmc as memcache
from controller import timeline, head2head, user, setting, player, data

urls = (
    '/', 'Index',
    '/account/signup', 'SignUp',
    '/account/signin', 'SignIn',
    '/account/signout', 'SignOut',
    '/account/find', 'Find',
    '/account/setting', 'Setting',
    '/setting/upload', 'Upload',
    '/live', 'Live',
    '/timeline', 'TimeLine',
    '/data', 'Data'
)

class Index:
    def GET(self):
        session.nav_index = 0
        top_points_players = player.top_players('currentrank')
        top_champion_players = player.top_players('championrank')
        top_popular_players = top_points_players
        return render.index(top_popular_players, top_points_players, top_champion_players)

class SignUp:
    def GET(self):
        session.nav_index = 5
        return render.signup()
    def POST(self):
        data = web.input(nick_name=None, email=None, password=None)
        username_c = user.check_nickname(data.username)
        password_c = user.check_password(data.password)
        email_c = user.check_email(data.email)
        web.header("Content-Type", "application/json")
        if username_c['status'] == 1 and password_c['status'] == 1 and email_c['status'] == 1:
            added = user.add_user(data.username, data.password, data.email)
            if added:
                return json.dumps({'status': 1})
            else:
                return json.dumps({'status': 0, 'message': '插入数据异常'})
        else:
            return json.dumps({'status': -1, 'message': [username_c, password_c, email_c]})

class SignIn:
    def GET(self):
        session.nav_index = 6
        if session.login:
            raise web.seeother('/')
        else:
            return render.signin()
    def POST(self):
        data = web.input(email=None, password=None, remember='n')
        web.header("Content-Type", "application/json")
        user_info = user.check_login(data.email, data.password)
        if user_info:
            #if data.remember == 'y':
            web.config.session_parameters['timeout'] = 604800
            session.login = True
            session.user = user_info
            #cookie_name = web.config.session_parameters['cookie_name']
            #web.setcookie(cookie_name, web.cookies().get(cookie_name), 604800)
            return json.dumps({'status': 1})
        else:
            return json.dumps({'status': -1, 'message': '用户名或密码不对'})

class SignOut():
    def GET(self):
        session.login = False
        session.user = None
        session.kill()
        raise web.seeother('/')

class Find:
    def GET(self):
        session.nav_index = -1
        return render.find()

class Setting:
    def GET(self):
        session.nav_index = -1
        province_list = user.get_areas(2)
        city_name = session.user['CITY']
        if not city_name or city_name == '0':
            city_name = '合肥市'
            province_name = '安徽省'
        else:
            province_name = user.get_province_by_city(city_name)
        default_city_list = user.get_areas(3, province_name)
        return render.setting(province_list, default_city_list, province_name, city_name)
    def POST(self):
        data = web.input(province_name=None, city_name=None, photo_url=None, introduce=None)
        if data.province_name:
            province_name = data.province_name
            web.header("Content-Type", "application/json")
            return json.dumps(user.get_areas(3, province_name))
        else:
            city_name = data.city_name
            photo_url = data.photo_url
            introduce = data.introduce
            session.user['CITY'] = city_name
            session.user['PHOTO'] = photo_url
            session.user['INTRODUCE'] = introduce
            web.header("Content-Type", "application/json")
            return json.dumps(user.update_user(city_name, photo_url, introduce))


class Upload:
    def POST(self):
        data = web.input(u_file={})
        if 'u_file' in data:
            file_name = data.u_file.filename
            name, ext = os.path.splitext(file_name)
            if ext[1:] not in ['jpg', 'jpeg', 'png']:
                return None
            photo_url = user.upload_photo(data.u_file.file.read(), ext)
            return photo_url
        else:
            return None


class TimeLine:
    def GET(self):
        session.nav_index = 2
        data = web.input(player=None)
        if not data or not data.player:
            top_champion_players = player.top_players('championrank', 0, 10)
            return render.timeline(top_champion_players)
        else:
            player_id = data.player
            if player_id == 'top30':
                """player_json = mem_client.get('top_player_timeline')
                if not player_json:
                    player_json = timeline.top_timeline_json()
                    mem_client.set('top_player_timeline', player_json, 604800)"""
                player_json = timeline.top_timeline_json()
                return render.timelinetop30(player_json)
            else:
                """mem_key = str('player_%s' % player_id)
                player_json = mem_client.get(mem_key)
                if not player_json:
                    player_json = timeline.player_timeline_json(player_id)
                    mem_client.set(mem_key, player_json, 604800)"""
                player_json = timeline.player_timeline_json(player_id)
                return render.timelineplayer(player_json)
    def POST(self):
        data = web.input(keyword=None)
        if data.keyword:
            web.header("Content-Type", "application/json")
            return json.dumps(user.retrieve_user(data.keyword))

class Live:
    def GET(self):
        session.nav_index = 1
        player_json = head2head.player_info(4846, 11530)
        return render.live(player_json)

class Data:
    def GET(self):
        session.nav_index = 3
        pdata = web.input(country=None, tournament=None)
        if pdata.country:
            xlabel, ylabel, ylabel1 = data.get_country_highrank(pdata.country)
            xlabel2, ylabel2 = data.get_country_topcount(pdata.country)
            infos = data.get_country_info(pdata.country)
            return render.datacountry(infos, xlabel, ylabel, ylabel1, xlabel2, ylabel2)
        elif pdata.tournament:
            infos = data.get_tournament_info(pdata.tournament)
            return render.datatournament(infos)
        return render.data()
    def POST(self):
        pdata = web.input()
        web.header("Content-Type", "application/json")
        if pdata.keyword:
            return json.dumps(data.retrieve(pdata.keyword, pdata.category))

app = web.application(urls, globals())
store = web.session.DBStore(setting.db, 'sessions')
session = web.session.Session(app, store, initializer={'login': False, 'user': None, 'nav_index': 0})
app_root = os.path.dirname(__file__)
templates_root = os.path.join(app_root, 'templates')
render = web.template.render(templates_root, base='base', globals={'session': session})
mem_client = memcache.Client()
application = sae.create_wsgi_app(app.wsgifunc())