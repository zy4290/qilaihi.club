#! /usr/bin/env python3.5
# coding: utf-8


from tornado import ioloop
from tornado.options import define, options

from weixin import wxutil

define('debug', True, type=bool)
define('autoreload', True, type=bool)

if __name__ == '__main__':
    options.logging = 'debug'
    options.parse_command_line()

    # 立即刷新access_token
    ioloop.IOLoop.current().run_sync(wxutil.refresh_access_token)

    # 设置刷新access token定时任务
    ioloop.PeriodicCallback(wxutil.refresh_access_token,
                            2400 * 1000
                            ).start()

    ioloop.IOLoop.current().start()
