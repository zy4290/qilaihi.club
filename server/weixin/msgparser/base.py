#! /usr/bin/env python3.5
# coding: utf-8


class BaseMsgParser:

    async def _msg_save(self, xml_data):
        pass

    async def reply(self, xml):
        pass

    def parse(self, xml_data):
        pass

