#! /usr/bin/env python3.5
# coding: utf-8

import datetime
import json
import logging

from tornado import web, gen

from api.response import Response
from model.dbutil import DBUtil
from model.event import Event


class SearchEventByCodeHandler(web.RequestHandler):

    @staticmethod
    def query(code):
        events = Event.select().where(Event.code == code).dicts()
        result = {}
        for event in events:
            result = event
            break
        return result

    @gen.coroutine
    def post(self):
        try:
            request = json.loads(self.request.body.decode())
            code = request['code']
            logging.debug('code: {0}'.format(code))
            result = yield DBUtil.do(self.query, code)
            if result['status'] == -1:
                self.write(Response(
                    status=1, msg='sorry，亲，该活动已关闭',
                    result={}
                ).json())
            else:
                self.write(Response(
                    status=1, msg='ok',
                    result=json.dumps(result, ensure_ascii=False, indent=4)
                ).json())
        except Exception as e:
            self.write(Response().json())
            logging.exception('GetEventHandler error: {0}'.format(str(e)))


class CreateEventHandler(web.RequestHandler):
    @gen.coroutine
    def post(self):
        try:
            request = json.loads(self.request.body.decode())
            event = Event(
                code=request.get('code', None),
                status=0,
                logoimgurl=request.get('logoimgurl', None),
                title=request.get('title', None),
                time=request.get('time', None),
                aacost=request.get('aacost', None),
                tag=request.get('tag', None),
                agerange=request.get('agerange', None),
                location=request.get('location', None),
                latitude=request.get('latitude', None),
                longtitude=request.get('longtitude', None),
                createtime=datetime.datetime.now(),
                organizaerid=request.get('organizaerid', None)
            )
            yield DBUtil.do(event.save)
            self.write(Response(
                status=1, msg='恭喜你，活动发布成功！',
                result=None
            ).json())
        except Exception as e:
            self.write(Response().json())
            logging.exception('CreateEventHandler error: {0}'.format(str(e)))
