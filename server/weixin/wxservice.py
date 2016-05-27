#! /usr/bin/env python3.5
# coding: utf-8

from tornado import web


class WeiXinMessageHandler(web.RequestHandler):

    def get(self):
        signature = self.request.arguments['signature'][0]
        timestamp = self.request.arguments['timestamp'][0]
        nonce = self.request.arguments['nonce'][0]
        echostr = self.request.arguments['echostr'][0]

        self.write(echostr)
