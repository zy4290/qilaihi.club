#! /usr/bin/env python3.5
# coding: utf-8

from peewee import *

from model import basemodel


class Star(basemodel.BaseModel):
    eventid = IntegerField(null=True)
    eventcode = CharField(null=True)
    userid = IntegerField(null=True)
    openid = CharField(null=True)
    status = IntegerField(null=True)
    createtime = DateTimeField(null=True)
    updatetime = DateTimeField(null=True)

    class Meta:
        db_table = 'star'
        schema = 'qilaihi'
