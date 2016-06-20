#! /usr/bin/env python3.5
# coding: utf-8

import logging

from tornado import gen

from model import dbutil
from model.config import Config


@gen.coroutine
def get_baidu_api_url(query, region, output='json'):
    url = 'http://api.map.baidu.com/place/v2/search?q={0}&region={1}&output={2}&ak={3}'
    config = yield dbutil.do(Config.get)
    logging.debug(config.baiduak)
    return url.format(query, region, output, config.baiduak)
