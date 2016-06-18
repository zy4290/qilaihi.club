#! /usr/bin/env python3.5
# coding: utf-8

from tornado import gen

from model import dbutil


class BaseMsgHandler:
    @gen.coroutine
    def process(self, wxmsg):
        yield dbutil.do(wxmsg.save)
