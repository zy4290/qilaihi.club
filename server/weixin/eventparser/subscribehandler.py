#! /usr/bin/env python3.5
# coding: utf-8

import datetime

from playhouse import shortcuts
from tornado import gen

from model import dbutil
from model.user import User
from weixin import wxutil
from weixin.basemsghandler import BaseMsgHandler


class SubscribeHandler(BaseMsgHandler):
    @gen.coroutine
    def process(self, wxmsg):
        user = yield wxutil.get_user_info(wxmsg.fromusername)
        dbutil.do(shortcuts.dict_to_model(User, user).save)
        wxmsg.response, wxmsg.responsetime = 1, datetime.datetime.now()
        yield super().process(wxmsg)
