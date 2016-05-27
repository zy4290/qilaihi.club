#! /usr/bin/env python3.5
# coding: utf-8

from tornado import web


class WeiXinMessageHandler(web.RequestHandler):

    def get(self):
        signature = self.request.arguments['signature']
        timestamp = self.request.arguments['timestamp']
        nonce = self.request.arguments['nonce']
        echostr = self.request.arguments['echostr']

        self.write(echostr)
