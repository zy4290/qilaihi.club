#! /usr/bin/env python3.5
# coding: utf-8

from concurrent.futures import ThreadPoolExecutor

from tornado import gen
from tornado.web import RequestHandler

from model import dbutil

db = dbutil.get_db()


class DatabaseRequestHandler(RequestHandler):
    @gen.coroutine
    def prepare(self):
        yield ThreadPoolExecutor(1).submit(db.connect())
        return super(DatabaseRequestHandler, self).prepare()

    @gen.coroutine
    def on_finish(self):
        if not db.is_closed():
            yield ThreadPoolExecutor(1).submit(db.close())
        return super(DatabaseRequestHandler, self).on_finish()
