#! /usr/bin/env python3.5
# coding: utf-8

from peewee import *

from model import basemodel


class User(basemodel.BaseModel):
    nickname = CharField(null=True)
    sex = IntegerField(null=True)
    country = CharField(null=True)
    province = CharField(null=True)
    city = CharField(null=True)
    headimgurl = CharField(null=True)
    unionid = CharField(null=True)
    openid = CharField(null=True)
    priviledge = CharField(null=True)
    mobile = CharField(null=True)
    latidude = CharField(null=True)
    longtitude = CharField(null=True)
    precision = CharField(null=True)
    agerange = IntegerField(null=True)
    tagprefs = CharField(null=True)
    pushevent = IntegerField(null=True)
    showinfo = IntegerField(null=True)
    likecount = IntegerField(null=True)
    dislikecount = IntegerField(null=True)
    createtime = DateTimeField(null=True)
    updatetime = DateTimeField(null=True)

    class Meta:
        db_table = 'user'
        schema = 'qilaihi'
