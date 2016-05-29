#! /usr/bin/env python3.5
# coding: utf-8

import hashlib
import logging

from tornado import web, ioloop

from weixin import config
from weixin.msghandler.msgparser import MsgParser
from model.config import Config


class WeiXinMessageHandler(web.RequestHandler):

    @staticmethod
    def _validate(signature, timestamp, nonce, echostr):
        try:
            logging.debug(
                'signature:{0} timestamp:{1} nonce:{2} echostr:{3}'.
                format(signature, timestamp, nonce, echostr))
            token = Config().select().get().access_token()
            tmp_list = sorted([token, timestamp, nonce])
            tmp_str = ''.join(tmp_list)
            logging.debug('before sha1: {0}'.format(tmp_str))
            tmp_str = hashlib.sha1(tmp_str.encode()).hexdigest()
            logging.debug('after  sha1: {0}'.format(tmp_str))
            if tmp_str == signature:
                return True
            else:
                return False
        except Exception as e:
            logging.error(str(e))
            return False

    def get(self):
        try:
            signature = self.get_argument('signature')
            timestamp = self.get_argument('timestamp')
            nonce = self.get_argument('nonce')
            echostr = self.get_argument('echostr')
            valid = WeiXinMessageHandler._validate(signature, timestamp, nonce, echostr)
            if valid:
                self.write(echostr)
            else:
                self.write(config.success_response)
        except Exception as e:
            logging.error(str(e))
            self.write(config.error_response)

    def post(self):
        try:
            xml = self.request.body.decode()
            logging.debug(xml)
            self.write(config.success_response)
            ioloop.IOLoop.current().spawn_callback(
                MsgParser().parse, xml)
        except Exception as e:
            logging.error(str(e))
            self.write(config.error_response)
