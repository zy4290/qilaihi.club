#! /usr/bin/env python3.5
# coding: utf-8

from model import __param__


def get_db():
    return __param__.db(
        host=__param__.ip, port=__param__.port, user=__param__.user,
        password=__param__.password, database=__param__.database,
        charset=__param__.charset
    )
