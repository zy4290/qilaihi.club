#! /usr/bin/env python3.5
# coding: utf-8

import logging

from tornado import web, ioloop
from tornado.options import define, options

from api.v1 import eventservice
from api.v1 import lbsservice
from api.v1 import wxwebservice
from route import page
from weixin import wxservice

define('port', 8080, type=int)
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
        (r'/', page.HomeHandler),
        (r'/event.*', page.EventHandler),

        # HTTP API

        # 地址API
        (r'/api/v1/place/query', lbsservice.PlaceServiceHandler),

        # 活动API
        (r'/api/v1/event/list', eventservice.ListEventHandler),
        (r'/api/v1/event/publish', eventservice.PublishEventHandler),
        (r'/api/v1/event/get', eventservice.GetEventHandler),
        (r'/api/v1/event/query', eventservice.QueryEventHandler),

        # 微信页面 API
        (r'/api/v1/wxweb/user/get', wxwebservice.GetUserInfoHandler),
        (r'/api/v1/wxweb/url/sign', wxwebservice.SignatureHandler),

        # 微信服务入口
        (r'/weixin', wxservice.WeiXinMessageHandler),

        # 异常处理
        (r'/.*', page.PageNotFoundHandler)

    ], **settings)

    application.listen(options.port)
    logging.debug('server started.')
    ioloop.IOLoop.current().start()

