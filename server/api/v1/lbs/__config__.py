#! /usr/bin/env python3.5
# coding: utf-8
from urllib import parse


def get_baidu_ak():
    return '4dbe2ddacb82cc8360444cddac6c62f2'


def get_baidu_api_url(query, region, output='json'):
    return 'http://api.map.baidu.com/place/v2/search?q=' + \
        parse.quote(query) + '&region=' + \
        parse.quote(region) + '&output=' + \
        output + '&ak=' + get_baidu_ak()
