#! /usr/bin/env python3.5
# coding: utf-8

import datetime
import logging

import peewee
from peewee import *
from playhouse import shortcuts
from tornado import gen
from xpinyin import Pinyin

from model import dbutil
from model.event import Event
from weixin import wxutil


@gen.coroutine
def create_qrcode(event):
    event.qrcodeurl = yield wxutil.get_temp_qrcode_url(event.get_id())
    event.qrcodecreatetime = datetime.datetime.now()
    yield dbutil.do(event.save)


@gen.coroutine
def query_by_code(code):
    try:
        event = Event.get(Event.code == code)
        result = shortcuts.model_to_dict(event)
    except peewee.DoesNotExist:
        result = {}
    return result


@gen.coroutine
def query_fulltext_code(code):
    pinyin = Pinyin()
    initials = []
    for letter in pinyin.get_initials(code, splitter=' ').lower().split(' '):
        if letter.isalpha():
            initials.append(letter * 4)
    logging.debug(initials)
    analysed_code = pinyin.get_pinyin(code, splitter=u' ') + ' ' + ' '.join(initials)
    logging.debug(analysed_code)
    clause = "MATCH(`codepinyin`, `codepinyininitials`) AGAINST (%s)"
    query = yield dbutil.do(Event.select(SQL('*, ' + clause + ' AS similarity', analysed_code)).where(
        SQL(clause, analysed_code)).limit(4).dicts)
    events = [event for event in query]
    logging.debug(events)
    return events
