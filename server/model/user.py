#! /usr/bin/env python3.5
# coding: utf-8

from peewee import *

from model import basemodel


class User(basemodel.BaseModel):
    agerange = IntegerField(null=True)
    city = CharField(null=True)
    country = CharField(null=True)
    createtime = DateTimeField(null=True)
    dislikecount = IntegerField(null=True)
    groupid = IntegerField(null=True)
    headimgurl = CharField(null=True)
    latitude = CharField(null=True)
    likecount = IntegerField(null=True)
    longitude = CharField(null=True)
    mobile = CharField(null=True)
    nickname = CharField(null=True)
    openid = CharField(unique=True)
    precision = CharField(null=True)
    privilege = CharField(null=True)
    province = CharField(null=True)
    pushevent = IntegerField(null=True)
    remark = CharField(null=True)
    sex = IntegerField(null=True)
    showinfo = IntegerField(null=True)
    subscribe = IntegerField(null=True)
    subscribe_time = IntegerField(null=True)
    tagprefs = CharField(null=True)
    unionid = CharField(null=True)
    updatetime = DateTimeField(null=True)
    language = CharField(null=True)

    class Meta:
        db_table = 'user'
        schema = 'qilaihi'
