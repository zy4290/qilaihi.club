#! /usr/bin/env python3.5
# coding: utf-8

from tornado import web
import hashlib
import logging


class WeiXinMessageHandler(web.RequestHandler):

    def get(self):
        signature = self.get_argument('signature')
        timestamp = self.get_argument('timestamp')
        nonce = self.get_argument('nonce')
        echostr = self.get_argument('echostr')
        # signature = self.request.query_arguments['signature'][0].decode()
        # timestamp = self.request.query_arguments['timestamp'][0].decode()
        # nonce = self.request.query_arguments['nonce'][0].decode()
        # echostr = self.request.query_arguments['echostr'][0].decode()
        logging.info(
            'signature:{0} timestamp:{1} nonce:{2} echostr:{3}'.
            format(signature, timestamp, nonce, echostr))
        token = 'qilaihiclubweixinservice'
        tmp_list = sorted([token, timestamp, nonce])
        tmp_str = ''.join(tmp_list)
        logging.debug('before sha1: {0}'.format(tmp_str))
        tmp_str = hashlib.sha1(tmp_str.encode()).hexdigest()
        logging.debug('after  sha1: {0}'.format(tmp_str))
        if tmp_str == signature:
            self.write(echostr)
        else:
            self.write('-1')
