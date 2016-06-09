#! /usr/bin/env python3.5
# coding: utf-8

import json
import logging

from playhouse.pool import PooledMySQLDatabase
from playhouse.shortcuts import RetryOperationalError


class RetryPooledMySQLDB(RetryOperationalError, PooledMySQLDatabase):
    pass


with open('dbparam.json') as config_file:
    dbparam = json.load(config_file)
logging.debug(dbparam)

db = RetryPooledMySQLDB
max_connection = dbparam.get('max_connection', 20)
stale_timeout = dbparam.get('stale_timeout', 600)
ip = dbparam.get('ip', 'localhost')
port = dbparam.get('port', 3306)
user = dbparam.get('user', 'user')
password = dbparam.get('password', 'password')
database = dbparam.get('database', 'mysql')
charset = dbparam.get('charset', 'utf8')
