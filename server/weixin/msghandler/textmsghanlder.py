#! /usr/bin/env python3.5
# coding: utf-8

from tornado import gen

from weixin.basemsghandler import BaseMsgHandler


class TextMsgHandler(BaseMsgHandler):
    @gen.coroutine
    def geteventbycode(self, code):
        pass

    @gen.coroutine
    def gethongbaocode(self):
        pass

    @gen.coroutine
    def getprefevents(self):
        pass

    @gen.coroutine
    def process(self, wxmsg):
        pass
