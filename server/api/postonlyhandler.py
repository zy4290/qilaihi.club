#! /usr/bin/env python3.5
# coding: utf-8

from tornado import web

from api.response import Response


class PostOnlyHandler(web.RequestHandler):
    def get(self):
        self.write(Response(msg='sorry，亲，接口只允许http post请求').json())
