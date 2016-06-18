#! /usr/bin/env python3.5
# coding: utf-8

import logging
from datetime import datetime
from xml.etree import ElementTree

from tornado import gen

from model.wxmessage import WXMessage
from weixin.eventparser.locationhandler import LocationHandler
from weixin.eventparser.subscribehandler import SubscribeHandler
from weixin.eventparser.unsubscribehandler import UnSubscribeHandler
from weixin.msghandler.textmsghanlder import TextMsgHandler

msg_handler_map = {
    'text': TextMsgHandler(),
    'image': None,
    'voice': None,
    'video': None,
    'shortvideo': None,
    'location': None,
    'link': None
}

event_handler_map = {
    'subscribe': SubscribeHandler(),
    'unsubscribe': UnSubscribeHandler(),
    'SCAN': None,
    'LOCATION': LocationHandler(),
    'CLICK': None,
    'VIEW': None
}


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

        try:
            if wxmsg.msgtype != 'event':
                msg_handler = msg_handler_map.get(wxmsg.msgtype, None)
                if msg_handler:
                    yield msg_handler.process(wxmsg)
                else:
                    logging.warning('检测到未注册的消息类型：{0} 消息体:{1}'.format(wxmsg.msgtype, xml))
            else:
                event_handler = event_handler_map.get(wxmsg.event, None)
                if event_handler:
                    yield event_handler.process(wxmsg)
                else:
                    logging.warning('检测到未注册的事件类型：{0} 消息体:{1}'.format(wxmsg.event, xml))
        except Exception as e:
            logging.exception('处理消息发生异常：{0}，异常消息：{1}'.format(xml, str(e)))
            # finally:
            #    yield dbutil.do(wxmsg.save)
