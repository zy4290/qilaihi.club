#! /usr/bin/env python3.5

from tornado import web


class HomePageHandler(web.RequestHandler):

    def get(self):
        self.write("hello api v1")
