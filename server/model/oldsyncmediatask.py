#! /usr/bin/env python3.5
# coding: utf-8

from peewee import *

from model import basemodel


class OldSyncMediaTask(basemodel):
    createtime = DateTimeField(null=True)
    eventid = IntegerField(null=True)
    localpath = CharField(null=True)
    mediaid = CharField(null=True)
    ossurl = CharField(null=True)
    status = IntegerField(null=True)
    updatetime = DateTimeField(null=True)

    class Meta:
        db_table = 'oldsyncmediatask'
        schema = 'qilaihi'
