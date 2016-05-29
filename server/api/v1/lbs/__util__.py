#! /usr/bin/env python3.5
# coding: utf-8

from tornado.escape import url_escape

from model.config import Config


def _get_baidu_ak():
    return Config.select().get().baiduak


def get_baidu_api_url(query, region, output='json'):
    url = 'http://api.map.baidu.com/place/v2/search?q={0}&region={1}&output={2}&ak={3}'
    url.format(query, region, output, _get_baidu_ak())
    return url.format(query, region, output, _get_baidu_ak())

