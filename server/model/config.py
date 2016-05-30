#! /usr/bin/env python3.5
# coding: utf-8

from peewee import *

from model import basemodel


class Config(basemodel.BaseModel):
    accesstoken = CharField(null=True)
    expires = IntegerField(null=True)
    appsecret = CharField(null=True)
    appid = CharField(null=True)
    token = CharField(null=True)
    encodingaeskey = CharField(null=True)
    baiduak = CharField(null=True)

    class Meta:
        db_table = 'config'
        schema = 'qilaihi'
