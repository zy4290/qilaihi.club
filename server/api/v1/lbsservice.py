#! /usr/bin/env python3.5
# coding: utf-8

import json
import logging

from api.postonlyhandler import PostOnlyHandler
from api.response import Response
from service import place


class PlaceServiceHandler(PostOnlyHandler):

    async def post(self):
        try:
            request = json.loads(self.request.body.decode())
            query = request['query']
            region = request['region']
            logging.debug('query: {0} region: {1}'.format(query, region))
            response = await place.get(query, region)
            self.write(response)
        except Exception as e:
            self.write(Response().json())
            logging.exception('PlaceServiceHandler error: {0}'.format(str(e)))
