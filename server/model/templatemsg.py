#! /usr/bin/env python3.5
# coding: utf-8

from peewee import *

from model import basemodel


class Templatemsg(basemodel.BaseModel):
    createtime = DateTimeField(null=True)
    data = TextField(null=True)
    status = IntegerField(null=True)
    templateid = CharField(null=True)
    touser = CharField(null=True)
    updatetime = DateTimeField(null=True)
    url = CharField(null=True)
    msgid = CharField(null=True)

    class Meta:
        db_table = 'templatemsg'
        schema = 'qilaihi'
