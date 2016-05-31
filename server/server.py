#! /usr/bin/env python3.5
# coding: utf-8

import logging

from tornado import web, ioloop
from tornado.options import define, options

from api.v1 import placeservice
from route import page
from weixin import wxservice
from weixin import wxutil
from weixin.msghandler.msgdispatcher import MsgDispatcher

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
        (r'/api/v1/place', placeservice.PlaceServiceHandler),
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

    # 每2399秒刷新access token
    # TODO 多实例部署时需要挪出去
    ioloop.PeriodicCallback(wxutil.refresh_access_token,
                            2399 * 1000
                            ).start()

    ioloop.IOLoop.current().run_sync(wxutil.refresh_access_token)
    logging.debug('server started.')
    ioloop.IOLoop.current().start()

