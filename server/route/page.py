#! /usr/bin/env python3.5
# -*- coding: utf-8 -*-

from tornado import web


class DefaultHandler(web.RequestHandler):
    def get(self):
        self.write('404 Page Not Found')

    def write_error(self, status_code, **kwargs):
        if status_code == 404:
            self.write('404 Page Not Found')
        elif status_code == 500:
            self.write('500 Server Internal Error')
        else:
            self.write(status_code)


class HomePageHandler(web.RequestHandler):

    def get(self):
        self.write("hello world")


class EventPageHandler(web.RequestHandler):

    def get(self):
        self.write("hello event")

