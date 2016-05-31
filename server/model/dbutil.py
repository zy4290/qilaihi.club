#! /usr/bin/env python3.5
# coding: utf-8

import logging

from tornado import gen

from model import __param__

db = __param__.db(
    __param__.database, max_connections=__param__.max_connection,
    stale_timeout=__param__.stale_timeout,
    host=__param__.ip, port=__param__.port, user=__param__.user,
    password=__param__.password, charset=__param__.charset)


class DBUtil:

    @staticmethod
    def get_db():
        return db

    @staticmethod
    @gen.coroutine
    def do(query, *args):
        try:
            db.connect()
            if len(args) == 0:
                result = query()
            else:
                result = query(args)
            return result
        finally:
            if not db.is_closed():
                db.close()
            else:
                logging.debug('db connection is closed.')
