#! /usr/bin/env python3.5
# coding: utf-8

import logging

from tornado import httpclient

from api.v1.lbs import __util__


def get(query, region):
    url = __util__.get_baidu_api_url(query, region)
    http_client = httpclient.HTTPClient()
    try:
        response = http_client.fetch(url)
        logging.debug(response.body.decode())
        return response.body.decode()
    except Exception as e:
        raise e
    finally:
        http_client.close()
