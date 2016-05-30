#! /usr/bin/env python3.5
# coding: utf-8

import logging

from tornado import web, escape

from api.response import Response
from api.v1.lbs import place


class PlaceServiceHandler(web.RequestHandler):

    async def post(self):
        try:
            request = escape.json_decode(self.request.body.decode())
            query = request['query']
            region = request['region']
            logging.debug('query: {0} region: {1}'.format(query, region))
            response = await place.get(query, region)
            self.write(response)
        except Exception as e:
            logging.error(str(e))
            self.write(Response().json())
