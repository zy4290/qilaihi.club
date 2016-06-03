#! /usr/bin/env python3.5
# coding: utf-8

import logging

from tornado import web, ioloop
from tornado.options import define, options

from api.v1.eventservice import ListEventHandler, PublishEventHandler, GetEventHandler
from api.v1.lbsservice import PlaceServiceHandler
from weixin import wxservice
from route import page

define('port', 80, type=int)
define('debug', True, type=bool)
define('autoreload', True, type=bool)

if __name__ == "__main__":
    options.logging = 'debug'
    options.parse_command_line()
    settings = {
        'debug': options.debug,
        'autoreload': options.autoreload
    }

    application = web.Application([
        # 页面路由
        # (r'/', page.HomePageHandler),

        # HTTP API

        # 地址API
        (r'/api/v1/place/query', PlaceServiceHandler),

        # 活动API
        (r'/api/v1/event/list', ListEventHandler),
        (r'/api/v1/event/publish', PublishEventHandler),
        (r'/api/v1/event/get', GetEventHandler),

        # 微信服务入口
        (r'/weixin', wxservice.WeiXinMessageHandler),

        # 异常处理
        (r'/.*', page.DefaultHandler)

    ], **settings)

    application.listen(options.port)
    logging.debug('server started.')
    ioloop.IOLoop.current().start()

