#! /usr/bin/env python3.5

from tornado import web


class UserAPIHandler(web.RequestHandler):

    def post(self):
        self.write("hello user api")
