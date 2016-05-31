#! /usr/bin/env python3.5
# coding: utf-8

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
        return json.dumps(result, ensure_ascii=False, indent=4)

    @gen.coroutine
    def post(self):
        try:
            request = json.loads(self.request.body.decode())
            code = request['code']
            logging.debug('code: {0}'.format(code))
            response = yield DBUtil.do(self.query, code)
            self.write(Response(status=1, msg='ok', result=response))
        except Exception as e:
            self.write(Response().json())
            logging.exception('GetEventHandler error: {0}'.format(str(e)))


class CreateEventHandler(web.RequestHandler):
    pass
