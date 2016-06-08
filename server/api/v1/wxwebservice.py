#! /usr/bin/env python3.5
# coding: utf-8

import hashlib
import json
import logging
import random
import string
import time
import urllib.request

from tornado import gen

from api.postonlyhandler import PostOnlyHandler
from api.response import Response
from model.config import Config
from model.dbutil import DBUtil
from weixin import wxutil


class GetUserInfoHandler(PostOnlyHandler):
    @gen.coroutine
    def post(self):
        try:
            request = json.loads(self.request.body.decode())
            code = request['code']
            scope = request.get('scope', 'snsapi_base')
            web_access_code = yield wxutil.get_oauth2_access_code(code)
            if scope == 'snsapi_userinfo':
                user_info = yield wxutil.pull_user_info(web_access_code['openid'],
                                                        web_access_code['access_token'])
            elif scope == 'snsapi_base':
                user_info = yield wxutil.pull_user_info(web_access_code['openid'])
            else:
                raise AttributeError
            self.write(Response(
                status=1, msg='ok',
                result=user_info
            ).json())
        except Exception as e:
            self.write(Response(msg='sorry，亲，获取用户信息失败').json())
            logging.exception('GetUserInfoHandler error: {0}'.format(str(e)))


class SignatureHandler(PostOnlyHandler):
    @staticmethod
    def random_str(len=16):
        elements = list(string.ascii_letters + string.digits)
        random.shuffle(elements)
        return ''.join(elements[:len])

    @gen.coroutine
    def post(self):
        try:
            param = json.loads(self.request.body.decode())
            url = urllib.request.unquote(param['url'])
            if url.find('#') != -1:
                url = url[0:url.index('#')]
            jsapi_ticket = yield wxutil.get_jsapi_ticket()
            noncestr = self.random_str()
            timestamp = int(time.time())
            param = {
                'url': url,
                'timestamp': timestamp,
                'jsapi_ticket': jsapi_ticket,
                'noncestr': noncestr
            }
            tmp_str = '&'.join(['{0}={1}'.format(key, param[key]) for key in sorted(param.keys())])
            sha1 = hashlib.sha1(tmp_str.encode()).hexdigest()
            del param['jsapi_ticket']
            param['signature'] = sha1
            config = yield DBUtil.do(Config.get)
            param['appid'] = config.appid
            self.write(Response(
                status=1, msg='ok',
                result=param
            ).json())
        except Exception as e:
            self.write(Response(msg='sorry，亲，js api签名失败').json())
            logging.exception('GetUserInfoHandler error: {0}'.format(str(e)))
