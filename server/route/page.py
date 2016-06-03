#! /usr/bin/env python3.5
# -*- coding: utf-8 -*-

from tornado import web


class DefaultHandler(web.RequestHandler):
    def get(self):
        self.write_error(404)

    def write_error(self, status_code, **kwargs):
        self.set_status(status_code)


class HomePageHandler(web.RequestHandler):

    def get(self):
        self.write("hello world")


class EventPageHandler(web.RequestHandler):

    def get(self):
        self.write("hello event")

