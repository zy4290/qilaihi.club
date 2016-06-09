#! /usr/bin/env python3.5
# coding: utf-8

import datetime
import json
import logging

import peewee
from playhouse.shortcuts import dict_to_model, model_to_dict
from tornado import gen

from api.postonlyhandler import PostOnlyHandler
from api.response import Response
from model import dbutil
from model.event import Event


class GetEventHandler(PostOnlyHandler):  # 按番号查询活动

    @staticmethod
    def query(code):
        try:
            event = Event.get(Event.code == code)
            result = model_to_dict(event)
        except peewee.DoesNotExist:
            result = {}
        return result

    @gen.coroutine
    def post(self):
        try:
            request = json.loads(self.request.body.decode())
            code = request['code']
            logging.debug('code: {0}'.format(code))
            result = yield dbutil.do(self.query, code)
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


class PublishEventHandler(PostOnlyHandler):  # 创建活动

    @gen.coroutine
    def post(self):
        try:
            data = json.loads(self.request.body.decode())
            logging.debug(data)
            event = dict_to_model(Event, data)
            event.createtime = datetime.datetime.now()
            result = yield dbutil.do(event.save)
            assert result == 1
            self.write(Response(
                status=1, msg='恭喜你，活动发布成功！',
                result={}
            ).json())
        except Exception as e:
            self.write(Response(msg='sorry，亲，活动发布失败').json())
            logging.exception('CreateEventHandler error: {0}'.format(str(e)))


class ListEventHandler(PostOnlyHandler):  # 分页查询活动列表

    # logger = logging.getLogger('ListEventHandler')

    @gen.coroutine
    def post(self):
        try:
            data = json.loads(self.request.body.decode())
            # self.logger.log(logging.DEBUG, data)
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
