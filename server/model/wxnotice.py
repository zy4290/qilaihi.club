#! /usr/bin/env python3.5
# coding: utf-8

from peewee import *

from model import basemodel


class Wxnotice(basemodel.BaseModel):
    wxtemplateid = IntegerField(null=True)
    openid = CharField(null=True)
    replycontent = CharField(null=True)
    createtime = DateTimeField(null=True)
    replytime = DateTimeField(null=True)
    status = IntegerField(null=True)
    wxresponse = CharField(null=True)
    errorcount = IntegerField(null=True)

    class Meta:
        db_table = 'wxnotice'
        schema = 'qilaihi'
