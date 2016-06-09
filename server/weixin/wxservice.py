#! /usr/bin/env python3.5
# coding: utf-8

import hashlib
import logging

from tornado import web, ioloop, gen

from config import wx as wxconfig
from model import dbutil
from model.config import Config
from weixin.msghandler.msgparser import MsgParser


class WeiXinMessageHandler(web.RequestHandler):

    @staticmethod
    @gen.coroutine
    def _validate(signature, timestamp, nonce, echostr):
        try:
            logging.debug(
                'signature:{0} timestamp:{1} nonce:{2} echostr:{3}'.
                format(signature, timestamp, nonce, echostr))
            _config = yield dbutil.do(Config().select().get)
            tmp_list = sorted([_config.token, timestamp, nonce])
            tmp_str = ''.join(tmp_list)
            logging.debug('before sha1: {0}'.format(tmp_str))
            tmp_str = hashlib.sha1(tmp_str.encode()).hexdigest()
            logging.debug('after  sha1: {0}'.format(tmp_str))
            if tmp_str == signature:
                return True
            else:
                return False
        except Exception as e:
            logging.exception('WeiXinMessageHandler error: {0}'.format(str(e)))
            return False

    @gen.coroutine
    def get(self):
        try:
            signature = self.get_argument('signature')
            timestamp = self.get_argument('timestamp')
            nonce = self.get_argument('nonce')
            echostr = self.get_argument('echostr')
            valid = yield WeiXinMessageHandler._validate(signature, timestamp, nonce, echostr)
            if valid:
                self.write(echostr)
            else:
                self.write(wxconfig.error_response)
        except Exception as e:
            self.write(wxconfig.error_response)
            logging.exception('WeiXinMessageHandler error: {0}'.format(str(e)))

    @gen.coroutine
    def post(self):
        try:
            xml = self.request.body.decode()
            logging.debug(xml)
            self.write(wxconfig.success_response)
            ioloop.IOLoop.current().spawn_callback(
                MsgParser().parse, xml)
        except Exception as e:
            self.write(wxconfig.error_response)
            logging.exception('WeiXinMessageHandler error: {0}'.format(str(e)))
