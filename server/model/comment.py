#! /usr/bin/env python3.5
# coding: utf-8

from peewee import *

from model import basemodel


class Comment(basemodel.BaseModel):
    eventid = IntegerField(null=True)
    userid = IntegerField(null=True)
    likecount = IntegerField(null=True)
    commenton = IntegerField(null=True)
    createtime = DateTimeField(null=True)

    class Meta:
        db_table = 'comment'
        schema = 'qilaihi'
