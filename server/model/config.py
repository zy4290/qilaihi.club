#! /usr/bin/env python3.5
# coding: utf-8

from peewee import *

from model import dbutil

"""
CREATE TABLE `config` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `accesstoken` varchar(100) DEFAULT NULL,
  `expires` int(11) DEFAULT NULL,
  `appsecret` varchar(100) DEFAULT NULL,
  `appid` varchar(100) DEFAULT NULL,
  `token` varchar(100) DEFAULT NULL,
  `encodingaeskey` varchar(100) DEFAULT NULL,
  `baiduak` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
"""

db = dbutil.get_db()


class Config(Model):
    id = IntegerField()
    accesstoken = CharField()
    expires = IntegerField()
    appsecret = CharField()
    appid = CharField()
    token = CharField()
    encodingaeskey = CharField()
    baiduak = CharField()

    class Meta:
        database = db
