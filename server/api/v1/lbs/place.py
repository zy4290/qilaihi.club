#! /usr/bin/env python3.5
# coding: utf-8

from api.v1.lbs import __util__
from tornado import httpclient


async def get(query, region):
    url = __util__.get_baidu_api_url(query, region)
    http_client = httpclient.AsyncHTTPClient()
    try:
        response = await http_client.fetch(url)
        return response.body
    except Exception as e:
        raise e
    finally:
        http_client.close()
