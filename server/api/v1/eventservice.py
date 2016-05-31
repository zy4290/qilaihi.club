#! /usr/bin/env python3.5
# coding: utf-8

import logging
import json

from tornado import web, gen

from api.response import Response
from model.dbutil import DBUtil
from model.event import Event


class GetEventHandler(web.RequestHandler):

    @staticmethod
    def query(code):
        return Event.get(Event.code == code)

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
            logging.exception('PlaceServiceHandler error: {0}'.format(str(e)))
