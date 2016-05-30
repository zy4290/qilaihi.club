#! /usr/bin/env python3.5
# coding: utf-8

import copy
import logging
from concurrent.futures import ThreadPoolExecutor

from tornado import gen
from tornado.escape import json_decode
from tornado.httpclient import AsyncHTTPClient

from model import dbutil
from model.config import Config
from weixin.config import access_token_url, custom_msg_url


@gen.coroutine
def refresh_access_token():
    config = yield ThreadPoolExecutor(1).submit(Config().select().get())
    try:
        http_client = AsyncHTTPClient()
        logging.debug(access_token_url.format(config.appid, config.appsecret))
        response = yield http_client.fetch(
            access_token_url.format(config.appid, config.appsecret))
        logging.debug(response.body.decode())
        result = json_decode(response.body.decode)
        config.accesstoken = result['access_token']
        config.expires = result['expires_in']
        dbutil.get_db().connect()
        yield ThreadPoolExecutor(1).submit(config.save())
    except Exception as e:
        raise e
    finally:
        if not dbutil.get_db().is_closed():
            dbutil.get_db().close()


@gen.coroutine
def get_access_token():
    config = Config().select().get()
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

    url = ''
    try:
        dbutil.get_db().connect()
        config = yield ThreadPoolExecutor(1).submit(Config().select().get)
        url = custom_msg_url.format(config.accesstoken)
    except Exception as e:
        logging.error(str(e))
    finally:
        if not dbutil.get_db().is_closed():
            dbutil.get_db().close()

    http_client = AsyncHTTPClient()
    yield http_client.fetch(url, **{'body': custom_text})
