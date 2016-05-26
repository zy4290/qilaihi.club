#! /usr/bin/env python3.5
# coding: utf-8

import __config__
from urllib import request
import json


def get(query, region):
    url = __config__.get_baidu_api_url(query, region)
    print(url)
    response = request.urlopen(url)
    if response:
        result = response.read().decode()
        response.close()
    return json.loads(result)['results']
