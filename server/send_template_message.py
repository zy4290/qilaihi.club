#! /usr/bin/env python3.5
# coding: utf-8


from tornado import gen
from tornado import ioloop
from tornado.options import options

from model.dbutil import DBUtil
from model.templatemsgtask import TemplatemsgTask
from weixin import wxutil


@gen.coroutine
def send_template_msg_task():
    while True:
        try:
            job = yield DBUtil.do(TemplatemsgTask.select().order_by(+TemplatemsgTask.createtime).get)
            yield wxutil.send_template_msg(job)
        finally:
            yield gen.sleep(0.1)


if __name__ == '__main__':
    options.logging = 'debug'
    options.parse_command_line()
    ioloop.IOLoop.current().spawn_callback(send_template_msg_task)
    ioloop.IOLoop.current().start()
