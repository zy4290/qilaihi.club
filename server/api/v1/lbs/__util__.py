#! /usr/bin/env python3.5
# coding: utf-8

from tornado.escape import url_escape

from model.config import Config


def _get_baidu_ak():
    return Config.select().get().baiduak


def get_baidu_api_url(query, region, output='json'):
    return 'http://api.map.baidu.com/place/v2/search?q=' + \
            url_escape(query) + '&region=' + url_escape(region) + \
            '&output=' + output + '&ak=' + _get_baidu_ak()
