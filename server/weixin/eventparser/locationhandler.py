#! /usr/bin/env python3.5
# coding: utf-8

import datetime
from xml.etree import ElementTree

from tornado import gen

from model import dbutil
from model.user import User
from weixin.basemsghandler import BaseMsgHandler


class LocationHandler(BaseMsgHandler):
    @gen.coroutine
    def process(self, wxmsg):
        user = yield dbutil.do(User.select().where(User.openid == wxmsg.fromusername).get)
        xml_data = ElementTree.fromstring(wxmsg.content)
        user.latitude = xml_data.find('Latitude').text
        user.longitude = xml_data.find('Longitude').text
        user.precision = xml_data.find('Precision').text
        user.updatetime = datetime.datetime.now()
        yield dbutil.do(user.save)
        wxmsg.response, wxmsg.responsetime = 1, datetime.datetime.now()
        yield super().process(wxmsg)
