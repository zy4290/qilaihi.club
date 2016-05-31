#! /usr/bin/env python3.5
# coding: utf-8

import logging, datetime

from tornado import gen
from tornado.ioloop import IOLoop

from model import dbutil
from model.oldwxmessage import Oldwxmessage
from model.wxmessage import WXMessage
from weixin import wxutil


class MsgDispatcher:

    @staticmethod
    @gen.coroutine
    def _stash_msg(msg):
        if not isinstance(msg, WXMessage) or msg is None:
            return
        old_msg = Oldwxmessage(
            content=msg.content,
            tousername=msg.tousername,
            fromusername=msg.fromusername,
            createtime=msg.createtime,
            msgtype=msg.msgtype,
            event=msg.event,
            response=msg.response,
            responsetime=msg.responsetime,
            msgid=msg.msgid,
            msg=msg.msg
        )
        yield [dbutil.DBUtil().do(old_msg.save), dbutil.DBUtil().do(msg.delete_instance)]
        logging.debug('move msg to old.')

    @staticmethod
    @gen.coroutine
    def process():
        while True:
            db_util = dbutil.DBUtil()
            try:
                # retrieve un-responded message
                msg = yield db_util.do(WXMessage.select().order_by(WXMessage.createtime.asc()).limit(1).get)
                if msg is None:
                    continue
                # respond accordingly
                # TODO 需要根据消息处置，此处只是为了调试
                yield wxutil.send_custom_msg(msg, '你发送的是: {0}'.format(msg.content))
                msg.response = 1
                msg.responsetime = datetime.datetime.now()
                # stash msg
                IOLoop.current().spawn_callback(MsgDispatcher._stash_msg, msg)
            except Exception:
                continue
            finally:
                yield gen.sleep(0.1)
                # if not db_util.get_db().is_closed():
                #    db_util.get_db().close()
