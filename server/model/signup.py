#! /usr/bin/env python3.5
# coding: utf-8

from peewee import *

from model import basemodel


class Signup(basemodel.BaseModel):
    eventid = IntegerField(null=True)
    userid = IntegerField(null=True)
    status = IntegerField(null=True)
    createtime = DateTimeField(null=True)
    updatetime = DateTimeField(null=True)

    class Meta:
        db_table = 'signup'
        schema = 'qilaihi'
