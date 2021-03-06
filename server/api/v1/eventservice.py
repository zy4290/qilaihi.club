#! /usr/bin/env python3.5
# coding: utf-8

import datetime
import json
import logging

from playhouse.shortcuts import dict_to_model
from tornado import gen
from tornado import ioloop
from xpinyin import Pinyin

from api.postonlyhandler import PostOnlyHandler
from api.response import Response
from model import dbutil
from model.event import Event
from model.star import Star
from model.user import User
from service import event as event_service


class GetEventHandler(PostOnlyHandler):  # 按番号查询活动

    @gen.coroutine
    def post(self):
        try:
            request = json.loads(self.request.body.decode())
            code = request['code']
            logging.debug('code: {0}'.format(code))
            result = yield event_service.query_by_code(code)
            if result['status'] == -1:
                self.write(Response(
                    status=1, msg='sorry，亲，该活动已关闭',
                    result={}
                ).json())
            else:
                self.write(Response(
                    status=1, msg='ok',
                    result=result
                ).json())
        except Exception as e:
            self.write(Response(msg='sorry，亲，查询活动失败').json())
            logging.exception('GetEventHandler error: {0}'.format(str(e)))


class QueryEventHandler(PostOnlyHandler):  # 按番号模糊检索活动

    @gen.coroutine
    def post(self):
        try:
            request = json.loads(self.request.body.decode())
            code = request['code']
            logging.debug('code: {0}'.format(code))
            result = yield event_service.query_fulltext_code(code)
            self.write(Response(
                status=1, msg='ok',
                result=result
            ).json())
        except Exception as e:
            self.write(Response(msg='sorry，亲，查询活动失败').json())
            logging.exception('GetEventHandler error: {0}'.format(str(e)))


class PublishEventHandler(PostOnlyHandler):  # 创建活动

    @gen.coroutine
    def post(self):
        try:
            data = json.loads(self.request.body.decode())
            logging.debug(data)
            event = dict_to_model(Event, data)
            event.createtime = datetime.datetime.now()
            pinyin = Pinyin()
            event.codepinyin = pinyin.get_pinyin(event.code, splitter=' ')
            initials = []
            for letter in pinyin.get_initials(event.code, splitter=' ').lower().split(' '):
                if letter.isalpha():
                    initials.append(letter * 4)
            event.codepinyininitials = ' '.join(initials)
            yield dbutil.do(event.save)
            self.write(Response(
                status=1, msg='恭喜你，活动发布成功！',
                result={}
            ).json())
            ioloop.IOLoop.current().spawn_callback(event_service.create_qrcode, event)
        except Exception as e:
            self.write(Response(msg='sorry，亲，活动发布失败').json())
            logging.exception('CreateEventHandler error: {0}'.format(str(e)))


class ListEventHandler(PostOnlyHandler):  # 分页查询活动列表
    @gen.coroutine
    def post(self):
        try:
            data = json.loads(self.request.body.decode())
            logging.debug(data)
            # 默认查询第一页
            page_number = data.get('page_number', 1)
            # 默认每页显示4条数据
            items_per_page = data.get('items_per_page', 4)
            query = yield dbutil.do(
                Event.select().order_by(-Event.createtime).paginate(
                    page_number, items_per_page).dicts)
            result = [event for event in query]
            self.write(Response(status=1, msg='ok', result=result).json())
        except Exception as e:
            self.write(Response(msg='sorry，亲，活动查询失败').json())
            logging.exception('CreateEventHandler error: {0}'.format(str(e)))


class StarEventHandler(PostOnlyHandler):  # 关注活动
    @gen.coroutine
    def post(self):
        try:
            data = json.loads(self.request.body.decode())
            code = data['eventcode']
            openid = data['openid']
            star = None
            try:
                star = yield dbutil.do(Star.select().where(
                    (Star.eventcode == code) & (Star.openid == openid)
                ).get)
            except:
                pass
            if star:
                if star.status == 1:  # 已经关注
                    raise RuntimeError
                else:  # 已经取消关注
                    star.status = 1
                    star.updatetime = datetime.datetime.now()
            else:  # 首次关注
                results = yield [
                    dbutil.do(Event.select(Event.id, Event.code).where(Event.code == code).get),
                    dbutil.do(User.select(User.id, User.openid).where(User.openid == openid).get)
                ]
                event = results[0]
                user = results[1]
                star = Star(
                    eventid=event.get_id(),
                    eventcode=event.code,
                    userid=user.get_id(),
                    openid=user.openid,
                    createtime=datetime.datetime.now(),
                    status=1
                )
            yield dbutil.do(star.save)
            self.write(Response(status=1, msg='ok', result={}).json())
        except RuntimeError as e:
            self.write(Response(msg='sorry，亲，用户已经关注该活动').json())
            logging.exception('StarEventHandler error: {0}'.format(str(e)))
        except Exception as e:
            self.write(Response(msg='sorry，亲，关注活动失败').json())
            logging.exception('StarEventHandler error: {0}'.format(str(e)))


class UnStarEventHandler(PostOnlyHandler):  # 取消关注活动
    @gen.coroutine
    def post(self):
        try:
            data = json.loads(self.request.body.decode())
            code = data['eventcode']
            openid = data['openid']
            star = yield dbutil.do(Star.select().where(
                (Star.eventcode == code) & (Star.openid == openid)
            ).get)
            star.status = -1
            star.updatetime = datetime.datetime.now()
            yield dbutil.do(star.save)
            self.write(Response(status=1, msg='ok', result={}).json())
        except Exception as e:
            self.write(Response(msg='sorry，亲，取消关注活动失败').json())
            logging.exception('UnStarEventHandler error: {0}'.format(str(e)))
