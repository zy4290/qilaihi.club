#! /usr/bin/env python3.5
# -*- coding: utf-8 -*-

from tornado import web


class HomePageHandler(web.RequestHandler):

    def get(self):
        self.write("hello world")


class EventPageHandler(web.RequestHandler):

    def get(self):
        self.write("hello event")
