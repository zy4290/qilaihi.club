#! /usr/bin/env python3.5
# coding: utf-8

from tornado import web
import hashlib


class WeiXinMessageHandler(web.RequestHandler):

    def get(self):
        signature = str(self.request.arguments['signature'][0])
        timestamp = str(self.request.arguments['timestamp'][0])
        nonce = str(self.request.arguments['nonce'][0])
        echostr = str(self.request.arguments['echostr'][0])
        token = 'qilaihiclubweixinservice'
        tmp_list = [token, timestamp, nonce]
        tmp_list.sort()
        tmp_str = '%s%s%s' % tuple(tmp_list)
        tmp_str = hashlib.sha1(tmp_str).hexdigest()
        if tmp_str == signature:
            self.write(echostr)
        else:
            self.write('-1')
