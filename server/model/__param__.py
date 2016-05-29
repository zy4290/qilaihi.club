#! /usr/bin/env python3.5
# coding: utf-8

from playhouse.pool import PooledMySQLDatabase

db = PooledMySQLDatabase
max_connection = 100
stale_timeout = None
ip = 'qilaihi.me'
port = 3306
user = 'root'
password = '98027531z'
database = 'qilaihi'
charset = 'utf8'
