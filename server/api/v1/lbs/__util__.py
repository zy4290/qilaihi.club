#! /usr/bin/env python3.5
# coding: utf-8

from model.config import Config
from model.dbutil import DBUtil


def _get_baidu_ak():
    config = yield DBUtil.do(Config.select().get)
    return config.baiduak


def get_baidu_api_url(query, region, output='json'):
    url = 'http://api.map.baidu.com/place/v2/search?q={0}&region={1}&output={2}&ak={3}'
    return url.format(query, region, output, _get_baidu_ak())

