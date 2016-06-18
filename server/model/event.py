#! /usr/bin/env python3.5
# coding: utf-8

from peewee import *

from model import basemodel


class Event(basemodel.BaseModel):
    aacost = IntegerField(null=True)
    address = CharField(null=True)
    agerange = IntegerField(null=True)
    code = CharField(unique=True)
    createtime = DateTimeField(null=True)
    dislikecount = IntegerField(null=True)
    expectsignups = IntegerField(null=True)
    focuscount = IntegerField(null=True)
    imgurls = TextField(null=True)
    latitude = CharField(null=True)
    likecount = IntegerField(null=True)
    location = CharField(null=True)
    longitude = CharField(null=True)
    mediaids = TextField(null=True)
    organizerid = CharField(null=True)
    singupcount = IntegerField(null=True)
    status = IntegerField(null=True)
    syncfinish = IntegerField(null=True)
    syncstatus = TextField(null=True)
    tag = CharField(null=True)
    telephone = CharField(null=True)
    time = DateTimeField(null=True)
    title = CharField(null=True)
    updatetime = DateTimeField(null=True)
    viewcount = IntegerField(null=True)
    qrcodecreatetime = DateTimeField(null=True)
    qrcodeurl = CharField(null=True)

    class Meta:
        db_table = 'event'
        schema = 'qilaihi'
