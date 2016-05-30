#! /usr/bin/env python3.5
# coding: utf-8

from peewee import *

from model import basemodel


class Oldwxmessage(basemodel.BaseModel):
    content = CharField(null=True)
    tousername = CharField(null=True)
    fromusername = CharField(null=True)
    createtime = DateTimeField(null=True)
    msgtype = CharField(null=True)
    event = CharField(null=True)
    response = IntegerField(null=True)
    responsetime = DateTimeField(null=True)
    msgid = CharField(null=True)
    msg = CharField(null=True)

    class Meta:
        db_table = 'oldwxmessage'
        schema = 'qilaihi'
