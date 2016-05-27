#! /usr/bin/env python3.5
# coding: utf-8

from xml.etree import ElementTree
import hashlib
import logging

from tornado import web


class WeiXinMessageHandler(web.RequestHandler):

    @staticmethod
    def _validate(signature, timestamp, nonce, echostr):
        try:
            logging.debug(
                'signature:{0} timestamp:{1} nonce:{2} echostr:{3}'.
                format(signature, timestamp, nonce, echostr))
            token = 'qilaihiclubweixinservice'
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
            return True

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
                self.write('')
        except Exception as e:
            logging.error(str(e))
            self.write('')

    def post(self):
        xml = self.request.body.decode()
        logging.debug(xml)
        try:
            from weixin import config
            data = ElementTree.fromstring(xml)
            config.msg_type_dict[data.find('MsgType').text].parse(data)
            self.write('success')
        except Exception as e:
            self.write('')
            logging.error(str(e))