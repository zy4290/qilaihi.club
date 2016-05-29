#! /usr/bin/env python3.5
# coding: utf-8

import logging

from tornado.httpclient import HTTPClient
from tornado.escape import json_decode
from tornado import gen

from model.config import Config
from weixin.config import access_token_url


@gen.coroutine
def refresh_access_token():
    config = Config().select().get()
    try:
        http_client = HTTPClient()
        logging.debug(access_token_url.format(config.appid, config.appsecret))
        response = http_client.fetch(
            access_token_url.format(config.appid, config.appsecret))
        logging.debug(response.body.decode())
        result = json_decode(response.body.decode)
        config.accesstoken = result['access_token']
        config.expires = result['expires_in']
        config.save()
        return result['access_token']
    except Exception as e:
        raise e


async def get_access_token():
    config = Config().select().get()
    if config.accesstoken is not None:
        return config.accesstoken
    else:
        access_token = await refresh_access_token()
        return access_token


async def send_template_msg():
    # TODO 发送模板消息待完成
    pass
