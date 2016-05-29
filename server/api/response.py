#! /usr/bin/env python3.5
# coding: utf-8

from tornado.escape import json_encode


class Response:

    def __init__(self, status=-1, msg='error', result={}):
        self.status = status
        self.msg = msg
        self.result = result

    def dict(self):
        return {
            'status': self.status,
            'msg': self.msg,
            'result': self.result
        }

    def json(self):
        return json_encode(self.dict())
