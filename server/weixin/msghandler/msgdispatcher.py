#! /usr/bin/env python3.5
# coding: utf-8

import logging
from concurrent.futures import ThreadPoolExecutor

from tornado import gen
from tornado.ioloop import IOLoop

from model.wxmessage import WXMessage
from model.oldwxmessage import Oldwxmessage
from weixin import wxutil


class MsgDispatcher:

    @staticmethod
    async def _stash_msg(msg):
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

        try:
            await ThreadPoolExecutor(1).submit(old_msg.save())
        except Exception as e:
            logging.error(str(e))
        finally:
            await ThreadPoolExecutor(1).submit(msg.delete())

    @staticmethod
    async def process():
        while True:
            try:
                # retrieve un-responded message
                msg = await ThreadPoolExecutor(1).submit(
                    WXMessage().select().order_by(WXMessage.createtime.asc()).get())
                if msg is None:
                    continue

                # respond accordingly
                # TODO 需要根据消息处置，此处只是为了调试
                await wxutil.send_custom_msg(msg, '你发送的是: {0}'.format(msg.content))

                # stash msg
                IOLoop.current().spawn_callback(MsgDispatcher._stash_msg)
            except Exception as e:
                logging.error(str(e))
            finally:
                await gen.sleep(0.1)
