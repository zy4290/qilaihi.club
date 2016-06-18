#! /usr/bin/env python3.5
# coding: utf-8

from tornado import gen


class BaseMsgHandler:
    @gen.coroutine
    def process(self, wxmsg):
        raise NotImplementedError
