#! /usr/bin/env python3.5
# coding: utf-8

from peewee import *

from model import dbutil


class BaseModel(Model):
    class Meta:
        database = dbutil.get_db()
