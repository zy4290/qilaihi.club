#! /usr/bin/env python3.5
# coding: utf-8

from model import __param__

_db = __param__.db(
            __param__.database, max_connections=__param__.max_connection,
            stale_timeout=__param__.stale_timeout,
            host=__param__.ip, port=__param__.port, user=__param__.user,
            password=__param__.password, charset=__param__.charset
        )


def get_db():
    return _db

