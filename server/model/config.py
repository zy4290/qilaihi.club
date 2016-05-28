#! /usr/bin/env python3.5
# coding: utf-8

from peewee import *

from model import dbutil

db = dbutil.get_db()


class Config(Model):
    id = IntegerField()
    accesstoken = CharField()
    expires = IntegerField()
    appsecret = CharField()
    appid = CharField()
    token = CharField()
    encodingaeskey = CharField()
    baiduak = CharField()

    class Meta:
        database = db
