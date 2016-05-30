#! /usr/bin/env python3.5
# coding: utf-8

from peewee import *

from model import basemodel


class Focus(basemodel.BaseModel):
    eventid = CharField(null=True)
    userid = CharField(null=True)
    createtime = DateTimeField(null=True)

    class Meta:
        db_table = 'focus'
        schema = 'qilaihi'
