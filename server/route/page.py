#! /usr/bin/env python3.5
# -*- coding: utf-8 -*-

import os
import sys

from tornado import web


class PageNotFoundHandler(web.RequestHandler):
    def get(self):
        self.write_error(404)

    def write_error(self, status_code, **kwargs):
        self.set_status(status_code, 'Page Not Found')
        self.write('404 Page Not Found')


class HomeHandler(web.RequestHandler):
    def get(self):
        self.render(sys.path[0] + os.path.sep + 'webroot/index.html')


class EventHandler(web.RequestHandler):
    def get(self):
        self.render(sys.path[0] + os.path.sep + 'webroot/event.html')
