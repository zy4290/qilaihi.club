#! /usr/bin/env python3.5
# coding: utf-8

from concurrent.futures import ThreadPoolExecutor

from tornado.web import RequestHandler
from model import dbutil

db = dbutil.get_db()


class DatabaseRequestHandler(RequestHandler):

    async def prepare(self):
        await ThreadPoolExecutor(1).submit(db.connect())
        return super(DatabaseRequestHandler, self).prepare()

    async def on_finish(self):
        if not db.is_closed():
            await ThreadPoolExecutor(1).submit(db.close())
        return super(DatabaseRequestHandler, self).on_finish()
