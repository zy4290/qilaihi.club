#! /usr/bin/env python3.5
# coding: utf-8

import datetime

from tornado import gen

from model import dbutil
from model.user import User
from weixin.basemsghandler import BaseMsgHandler


class UnSubscribeHandler(BaseMsgHandler):
    @gen.coroutine
    def process(self, wxmsg):
        user = yield dbutil.do(User.select().where(User.openid == wxmsg.fromusername).get)
        user.subscribe = 0
        dbutil.do(user.save)
        wxmsg.response, wxmsg.responsetime = 1, datetime.datetime.now()
        yield super().process(wxmsg)
