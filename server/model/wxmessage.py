#! /usr/bin/env python3.5
# coding: utf-8

from peewee import *

from model import dbutil

"""
CREATE TABLE `wxmessage` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `content` varchar(2000) DEFAULT NULL,
  `tousername` varchar(200) DEFAULT NULL,
  `fromusername` varchar(200) DEFAULT NULL,
  `createtime` datetime DEFAULT NULL,
  `msgtype` varchar(100) DEFAULT NULL,
  `event` varchar(100) DEFAULT NULL,
  `response` int(1) DEFAULT NULL COMMENT '0 error\n1 success',
  `responsetime` datetime DEFAULT NULL,
  `msgid` varchar(100) DEFAULT NULL,
  `msg` varchar(4000) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
"""


class WXMessage(Model):
    id = IntegerField()
    content = CharField()
    tousername = CharField()
    fromusername = CharField()
    createtime = DateTimeField()
    msgtype = CharField()
    event = CharField()
    response = IntegerField()
    responsetime = DateTimeField()
    msg = CharField()
    msgid = CharField()

    class Meta:
        database = dbutil.get_db()
