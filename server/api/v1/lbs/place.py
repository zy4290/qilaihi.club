#! /usr/bin/env python3.5
# coding: utf-8

import __config__
from urllib import request
import json
import sys


def get(query, region):
    url = __config__.get_baidu_api_url(query, region)
    response = request.urlopen(url)
    if response:
        result = response.read().decode()
        response.close()
    return json.loads(result)['results']

if __name__ == '__main__':
    if len(sys.argv) != 3:
        raise Exception(sys.argv[0] + ' query region')
    print(get(sys.argv[1], sys.argv[2]))
