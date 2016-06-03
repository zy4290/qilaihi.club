#! /usr/bin/env python3.5
# -*- coding: utf-8 -*-

from tornado import web


class DefaultHandler(web.RequestHandler):
    def get(self):
        self.write_error(404)

    def write_error(self, status_code, **kwargs):
        self.set_status(status_code)
        if status_code == 404:
            self.write('404 - Page Not Found')
        elif status_code == 500:
            self.write('500 - Internal Server Error')
        else:
            self.write(status_code)


class HomePageHandler(web.RequestHandler):

    def get(self):
        self.write("hello world")


class EventPageHandler(web.RequestHandler):

    def get(self):
        self.write("hello event")

