#! /usr/bin/env python3.5
# coding: utf-8

from peewee import *

from model import basemodel


class Event(basemodel.BaseModel):
    code = CharField(unique=True)
    status = IntegerField(null=True)
    imgurls = TextField(null=True)
    title = CharField(null=True)
    viewcount = IntegerField(null=True)
    focuscount = IntegerField(null=True)
    time = DateTimeField(null=True)
    aacost = IntegerField(null=True)
    tag = CharField(null=True)
    singupcount = IntegerField(null=True)
    expectsignups = IntegerField(null=True)
    agerange = IntegerField(null=True)
    location = CharField(null=True)
    address = CharField(null=True)
    telephone = CharField(null=True)
    latitude = CharField(null=True)
    longitude = CharField(null=True)
    likecount = IntegerField(null=True)
    dislikecount = IntegerField(null=True)
    createtime = DateTimeField(null=True)
    updatetime = DateTimeField(null=True)
    organizerid = IntegerField(null=True)

    class Meta:
        db_table = 'event'
        schema = 'qilaihi'
