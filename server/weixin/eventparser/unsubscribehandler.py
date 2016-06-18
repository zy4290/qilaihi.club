#! /usr/bin/env python3.5
# coding: utf-8

from tornado import gen

from model import dbutil
from model.user import User
from weixin.basemsghandler import BaseMsgHandler


class UnSubscribeHandler(BaseMsgHandler):
    @gen.coroutine
    def process(self, wxmsg):
        user = yield dbutil.do(User.get(User.openid == wxmsg.fromusername))
        user.subscribe = 0
        dbutil.do(user.save)
