#! /usr/bin/env python3.5
# coding: utf-8

from tornado import web, ioloop
from tornado.options import define, options
from route import page
from weixin import wxservice
from api.v1 import httpapi

define('port', 80, type=int)
define('debug', True, type=bool)
define('autoreload', True, type=bool)

if __name__ == "__main__":
    options.parse_command_line()
    settings = {'debug': options.debug, 'autoreload': options.autoreload}
    application = web.Application([
        # 页面路由
        (r'/', page.HomePageHandler),
        (r'/event', page.EventPageHandler),
        # (r'/trace', page.EventPageHandler),
        # (r'/mine', page.EventPageHandler),

        # HTTP API
        # 地址API
        (r'/api/v1/place', httpapi.PlaceServiceHandler),
        # (r'/api/v1/geocoding', None),

        # 活动API
        # (r'/api/v1/listevent', None),
        # (r'/api/v1/publishevent', None),
        # (r'/api/v1/getevent', None),
        # (r'/api/v1/searchevent', None),

        # 用户API
        # (r'/api/v1/getuser', None),

        # 微信服务
        (r'/weixin', wxservice.WeiXinMessageHandler)
    ], **settings)
    application.listen(options.port)
    ioloop.IOLoop.current().start()
