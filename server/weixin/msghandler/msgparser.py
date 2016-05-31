#! /usr/bin/env python3.5
# coding: utf-8

import logging

from datetime import datetime
from xml.etree import ElementTree

from tornado import gen

from model import dbutil
from model.wxmessage import WXMessage


class MsgParser:

    @staticmethod
    def _text(element):
        if element is not None:
            return element.text
        else:
            return None

    @staticmethod
    @gen.coroutine
    def parse(xml):
        xml_data = ElementTree.fromstring(xml)
        _tousername = MsgParser._text(xml_data.find('ToUserName'))
        _fromusername = MsgParser._text(xml_data.find('FromUserName'))
        _timestamp = MsgParser._text(xml_data.find('CreateTime'))
        if _timestamp is not None:
            _createtime = datetime.fromtimestamp(float(_timestamp))
        else:
            _createtime = None
        _msgtype = MsgParser._text(xml_data.find('MsgType'))
        _content = MsgParser._text(xml_data.find('Content'))
        _msgid = MsgParser._text(xml_data.find('MsgId'))
        _event = MsgParser._text(xml_data.find('Event'))

        wxmsg = WXMessage.create(
            content=_content,
            tousername=_tousername,
            fromusername=_fromusername,
            createtime=_createtime,
            msgtype=_msgtype,
            event=_event,
            msgid=_msgid,
            msg=xml
        )

        db_util = dbutil.DBUtil()
        yield db_util.do(wxmsg.save)
        logging.debug('wxmessage saved.')

