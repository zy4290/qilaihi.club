#! /usr/bin/env python3.5
# coding: utf-8

from tornado import web
from tornado import escape

from api.v1.lbs import place


class PlaceServiceHandler(web.RequestHandler):

    def post(self):
        request = escape.json_decode(self.request.body.decode())
        query = request['query']
        region = request['region']
        self.write(place.get(query, region))
