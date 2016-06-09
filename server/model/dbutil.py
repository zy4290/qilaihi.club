#! /usr/bin/env python3.5
# coding: utf-8

import logging
from concurrent.futures import ThreadPoolExecutor

from tornado import gen

from config import db as dbconfig

db = dbconfig.db(
    database=dbconfig.database, host=dbconfig.ip,
    port=dbconfig.port, user=dbconfig.user,
    password=dbconfig.password, charset=dbconfig.charset)

executor = ThreadPoolExecutor(max_workers=8)


def get_db():
    return db


def _do(query, expr=None):
    try:
        get_db().connect()
        if expr:
            return query(expr)
        else:
            return query()
    finally:
        if not get_db().is_closed():
            get_db().close()
        else:
            logging.warning('db connection is closed.')


@gen.coroutine
def do(query, expr=None):
    result = yield executor.submit(_do, *(query, expr))
    return result
