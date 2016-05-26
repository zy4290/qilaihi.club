#! /usr/bin/env python3.5
# coding: utf-8

from api.v1.lbs import __config__
from urllib import request
import json
import sys


def get(query, region):
    url = __config__.get_baidu_api_url(query, region)
    response = request.urlopen(url)
    if response:
        result = response.read().decode()
        response.close()
    return result
