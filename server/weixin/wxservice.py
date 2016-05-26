#! /usr/bin/env python3.5
# -*- coding: utf-8 -*-

from tornado import web


class WeiXinMessageHandler(web.RequestHandler):

    def get(self):
        self.write("hello weixin")
