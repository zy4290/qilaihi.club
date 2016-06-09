#! /usr/bin/env python3.5
# coding: utf-8

from playhouse.pool import PooledMySQLDatabase
from playhouse.shortcuts import RetryOperationalError


class RetryPooledMySQLDB(RetryOperationalError, PooledMySQLDatabase):
    pass

db = RetryPooledMySQLDB
max_connection = 20
stale_timeout = 60
ip = 'qilaihi.me'
port = 3306
user = 'root'
password = '98027531z'
database = 'qilaihi'
charset = 'utf8'
