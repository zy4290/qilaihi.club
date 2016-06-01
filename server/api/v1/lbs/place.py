#! /usr/bin/env python3.5
# coding: utf-8

import json
import logging

from tornado import httpclient

from api.response import Response
from api.v1.lbs import __util__


async def get(query, region):
    url = __util__.get_baidu_api_url(query, region)
    http_client = httpclient.AsyncHTTPClient()
    try:
        response = await http_client.fetch(url)
        logging.debug(response.body.decode())
        result = json.loads(response.body.decode())
        if result['status'] == 0:
            result['status'] = 1
            return json.dumps(result, ensure_ascii=False, indent=4)
        else:
            return json.dumps(Response(
                status=-1,
                msg='sorry，亲，位置查询失败',
                result=None
            ), ensure_ascii=False, indent=4)
    finally:
        http_client.close()
