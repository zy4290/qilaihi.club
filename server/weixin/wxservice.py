#! /usr/bin/env python3.5
# coding: utf-8

from tornado import web
import hashlib
import logging


class WeiXinMessageHandler(web.RequestHandler):

    def get(self):
        signature = self.request.query_arguments['signature'][0]
        timestamp = self.request.query_arguments['timestamp'][0]
        nonce = self.request.query_arguments['nonce'][0]
        echostr = self.request.query_arguments['echostr'][0]
        logging.info(str('%s %s %s %s', signature, timestamp, nonce, echostr))
        token = 'qilaihiclubweixinservice'
        tmp_list = [token, timestamp, nonce]
        tmp_list.sort()
        tmp_str = '%s%s%s' % tuple(tmp_list)
        logging.info(tmp_str)
        tmp_str = hashlib.sha1(tmp_str.encode()).hexdigest()
        logging.info(tmp_str)
        if tmp_str == signature:
            self.write(echostr)
        else:
            self.write('-1')
