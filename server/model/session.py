#! /usr/bin/env python3.5
# coding: utf-8

from peewee import *

from model import basemodel


class Session(basemodel.BaseModel):
    id = CharField(primary_key=True)
    userid = CharField(null=True)
    loginflag = IntegerField(null=True)

    class Meta:
        db_table = 'session'
        schema = 'qilaihi'
