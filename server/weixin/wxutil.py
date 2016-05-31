#! /usr/bin/env python3.5
# coding: utf-8

import copy
import logging
import json

from tornado import gen
from tornado.httpclient import AsyncHTTPClient

from model.dbutil import DBUtil
from model.config import Config
from weixin.config import access_token_url, custom_msg_url


@gen.coroutine
def refresh_access_token():
    logging.info('开始刷新微信access token')
    config = yield DBUtil.do(Config.select().get)

    http_client = AsyncHTTPClient()
    logging.debug(access_token_url.format(config.appid, config.appsecret))
    response = yield http_client.fetch(
        access_token_url.format(config.appid, config.appsecret))
    logging.info(response.body.decode())
    result = json.loads(response.body.decode())
    config.accesstoken = result['access_token']
    logging.debug(config.accesstoken)
    config.expires = result['expires_in']
    logging.debug(config.expires)
    yield DBUtil.do(config.save)


@gen.coroutine
def get_access_token():
    config = yield DBUtil.do(Config.select().get)
    if config.accesstoken is not None:
        return config.accesstoken
    else:
        access_token = yield refresh_access_token()
        return access_token


def send_template_msg():
    # TODO 发送模板消息待完成
    pass


_custom_text = {
    'touser': None,
    'msgtype': 'text',
    'text': {
        'content': None
    }
}


@gen.coroutine
def send_custom_msg(msg, reply):
    custom_text = copy.deepcopy(_custom_text)
    custom_text['touser'] = msg.fromusername
    custom_text['text']['content'] = reply
    logging.debug(custom_text)

    config = yield DBUtil.do(Config.select().get)
    url = custom_msg_url.format(config.accesstoken)
    logging.debug(url)

    logging.debug(json.dumps(custom_text, ensure_ascii=False, indent=4))
    http_client = AsyncHTTPClient()
    response = yield http_client.fetch(url, **{'method': 'POST',
                                               'body': json.dumps(custom_text, ensure_ascii=False)})
    logging.debug(response.body.decode())
