#! /usr/bin/env python3.5
# coding: utf-8

import json


class Response:
    def __init__(self, status=-1, msg='sorry，亲，服务出错啦', result=None):
        self.status = status
        self.msg = msg
        self.result = result

    @staticmethod
    def handler(data):
        if hasattr(data, 'isoformat'):
            return data.isoformat()
        else:
            raise TypeError

    def dict(self):
        return {
            'status': self.status,
            'msg': self.msg,
            'result': self.result
        }

    def json(self):
        return json.dumps(
            self.dict(),
            default=self.handler,
            ensure_ascii=False,
            indent=4
        )

