#! /usr/bin/env python3.5
# coding: utf-8

import json


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
        return json.dumps(self.dict(), ensure_ascii=False, indent=4)
