#! /usr/bin/env python3.5
# coding: utf-8


import json
import logging
import time

from peewee import DoesNotExist
from tornado import gen
from tornado import ioloop
from tornado.options import options

from config import sync as syncconfig
from model import dbutil
from model.event import Event
from weixin import wxutil


@gen.coroutine
def sync_media_file():
    while True:
        cur_hour = int(time.strftime('%H'))
        if cur_hour >= syncconfig.start_at and cur_hour < syncconfig.stop_at:
            try:
                event = yield dbutil.do(Event.select().where(
                    (Event.syncfinish != 1) | (Event.syncfinish >> None)).order_by(+Event.createtime).get)
                logging.info('开始处理活动[#{0}] 的media文件'.format(event.code))
                if event.mediaids:
                    all = json.loads(event.mediaids)
                    logging.debug('all ' + str(all))
                    if event.syncstatus:
                        uploaded = json.loads(event.syncstatus)
                    else:
                        uploaded = []
                    if event.imgurls:
                        img_urls = json.loads(event.imgurls)
                    else:
                        img_urls = {}
                    to_upload = list(set(all) - set(uploaded))
                    logging.info('待处理media文件清单' + str(to_upload))
                    results = yield [wxutil.process_temp_resource(media_id) for media_id in to_upload]
                    for i in range(0, len(results)):
                        if results[i] is not None:
                            uploaded.append(to_upload[i])
                            img_urls[to_upload[i]] = results[i]
                    event.syncstatus = json.dumps(uploaded, ensure_ascii=False)
                    event.imgurls = json.dumps(img_urls, ensure_ascii=False)
                    logging.info('已完成media文件清单:' + str(uploaded))
                    if set(all) == set(uploaded):
                        logging.info('活动[#{0}] 所有media文件已完成'.format(event.code))
                else:
                    logging.info('mediaids不存在，没有media文件需要同步')
                event.syncfinish = 1
                yield dbutil.do(event.save)
            except DoesNotExist:
                logging.info('无待同步media文件, sleep...')
                yield gen.sleep(60 * 10)
            except Exception as e:
                logging.exception('同步media文件发生异常：{0}, 退出...'.format(str(e)))
                break
        else:
            yield gen.sleep(60 * 10)


if __name__ == '__main__':
    options.logging = 'debug'
    options.parse_command_line()
    ioloop.IOLoop.current().spawn_callback(sync_media_file)
    ioloop.IOLoop.current().start()
