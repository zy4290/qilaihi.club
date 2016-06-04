#! /usr/bin/env python3.5
# coding: utf-8

import logging
from concurrent.futures import ThreadPoolExecutor

from tornado import gen

from model import __param__

db = __param__.db(
    __param__.database, max_connections=__param__.max_connection,
    stale_timeout=__param__.stale_timeout,
    host=__param__.ip, port=__param__.port, user=__param__.user,
    password=__param__.password, charset=__param__.charset)

executor = ThreadPoolExecutor(max_workers=__param__.max_connection)

class DBUtil:

    @staticmethod
    def get_db():
        return db

    @staticmethod
    def _do(query, expr=None):
        try:
            db.connect()
            if expr:
                return query(expr)
            else:
                return query()
        finally:
            if not db.is_closed():
                db.close()
            else:
                logging.warning('db connection is closed.')

    @staticmethod
    @gen.coroutine
    def do(query, expr=None):
        result = yield executor.submit(DBUtil._do, *(query, expr))
        return result
