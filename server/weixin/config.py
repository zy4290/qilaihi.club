#! /usr/bin/env python3.5
# coding: utf-8

from weixin.msgparser import default, text, location, event

msg_type_dict = {
    'text': text.TextMsgParser,
    'image': default.DefaultMsgParser,
    'voice': default.DefaultMsgParser,
    'video': default.DefaultMsgParser,
    'shortvideo': default.DefaultMsgParser,
    'location': location.LocationMsgParser,
    'event': event.EventMsgParser
}

event_type_dict = {
    'subscribe': None,
    'unsubscribe': None,
    'SCAN': None,
}