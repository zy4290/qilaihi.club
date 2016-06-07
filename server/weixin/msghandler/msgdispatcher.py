#! /usr/bin/env python3.5
# coding: utf-8

import datetime
import logging

from playhouse import shortcuts
from tornado import gen
from tornado.ioloop import IOLoop

from model.dbutil import DBUtil
from model.oldwxmessage import Oldwxmessage
from model.wxmessage import WXMessage
from weixin import wxutil


class MsgDispatcher:

    @staticmethod
    @gen.coroutine
    def _stash_msg(msg):
        if not isinstance(msg, WXMessage) or msg is None:
            return
        old_msg = shortcuts.dict_to_model(Oldwxmessage, shortcuts.model_to_dict(msg))
        yield [DBUtil.do(old_msg.save), DBUtil.do(msg.delete_instance)]
        logging.debug('move msg to old.')

    @staticmethod
    @gen.coroutine
    def process(msg):
        # respond accordingly
        # TODO 需要根据消息处置，此处只是为了调试
        yield wxutil.send_custom_msg(msg, '你发送的是: {0}'.format(msg.content))
        msg.response = 1
        msg.responsetime = datetime.datetime.now()
        # stash msg
        IOLoop.current().spawn_callback(MsgDispatcher._stash_msg, msg)

