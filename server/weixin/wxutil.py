#! /usr/bin/env python3.5
# coding: utf-8

import copy
import datetime
import json
import logging
import os.path

from peewee import DoesNotExist
from playhouse.shortcuts import dict_to_model, model_to_dict
from tornado import gen
from tornado.httpclient import AsyncHTTPClient

from model.config import Config
from model.dbutil import DBUtil
from model.oldtemplatemsgtask import OldTemplatemsgTask
from model.templatemsgtask import TemplatemsgTask
from model.user import User
from weixin import config as wxconfig


@gen.coroutine
def refresh_access_token():
    logging.info('开始刷新微信access token')
    try:
        config = yield DBUtil.do(Config.select().get)
        http_client = AsyncHTTPClient()
        logging.debug(wxconfig.access_token_url.format(config.appid, config.appsecret))
        response = yield http_client.fetch(
            wxconfig.access_token_url.format(config.appid, config.appsecret))
        logging.info(response.body.decode())
        result = json.loads(response.body.decode())
        config.accesstoken = result['access_token']
        config.jsapiticket = yield refresh_jsapi_ticket(config.accesstoken)
        config.expires = result['expires_in']
        logging.debug(config.accesstoken)
        logging.debug(config.jsapiticket)
        logging.debug(config.expires)
        yield DBUtil.do(config.save)
    except Exception:
        pass


@gen.coroutine
def refresh_jsapi_ticket(access_token):
    get_jsapi_ticket_url = wxconfig.jsapi_ticket_url.format(access_token)
    http_client = AsyncHTTPClient()
    response = yield http_client.fetch(get_jsapi_ticket_url)
    logging.debug(response.body.decode())
    result = json.loads(response.body.decode())
    return result.get('ticket', None)


@gen.coroutine
def get_access_token():
    config = yield DBUtil.do(Config.get)
    return config.accesstoken


@gen.coroutine
def get_jsapi_ticket():
    config = yield DBUtil.do(Config.get)
    return config.jsapiticket


@gen.coroutine
def send_template_msg(templatemsg):
    if not isinstance(templatemsg, TemplatemsgTask) or templatemsg is None: return
    logging.info('wxutil.send_template_msg - 开始发送模板消息：{0}'.format(
        model_to_dict(templatemsg)))
    config = yield DBUtil.do(Config.get)
    url = wxconfig.custom_msg_url.format(config.accesstoken)
    data = {
        'touser': templatemsg.touser,
        'template_id': templatemsg.templateid,
        'url': templatemsg.url,
        'data': json.loads(templatemsg.data)
    }
    http_client = AsyncHTTPClient()
    response = yield http_client.fetch(url, **{'method': 'POST',
                                               'body': json.dumps(data, ensure_ascii=False)})
    result = json.loads(response.body.decode())
    errcode = result['errcode']
    if errcode == 0:
        templatemsg.msgid = result['msgid']
        templatemsg.updatetime = datetime.datetime.now()
        oldmsg = dict_to_model(OldTemplatemsgTask, model_to_dict(templatemsg))
        yield [DBUtil.do(oldmsg.save), DBUtil.do(templatemsg.delete_instance)]
    else:
        raise RuntimeError('wxutil.send_template_msg-发送模板消息失败，消息内容：{0}'.format(
            model_to_dict(templatemsg)))


@gen.coroutine
def send_custom_msg(msg, reply):
    custom_text = copy.deepcopy(wxconfig.custom_text_template)
    custom_text['touser'] = msg.fromusername
    custom_text['text']['content'] = reply
    logging.debug(custom_text)

    config = yield DBUtil.do(Config.select().get)
    url = wxconfig.custom_msg_url.format(config.accesstoken)
    logging.debug(url)

    logging.debug(json.dumps(custom_text, ensure_ascii=False, indent=4))
    http_client = AsyncHTTPClient()
    response = yield http_client.fetch(url, **{'method': 'POST',
                                               'body': json.dumps(custom_text, ensure_ascii=False)})
    logging.debug(response.body.decode())


@gen.coroutine
def get_oauth2_access_code(code):
    if code:
        return '{}'

    config = DBUtil.do(Config.get)
    appid = config.appid
    secret = config.appsecret
    oauth2_url = wxconfig.oauth2_access_token_url.format(appid, secret, code)
    http_client = AsyncHTTPClient()
    response = yield http_client.fetch(oauth2_url)
    logging.debug(response.body.decode())
    return json.loads(response.body.decode())


@gen.coroutine
def refresh_oauth2_access_code(refresh_token):
    if refresh_access_token:
        return '{}'

    config = DBUtil.do(Config.get)
    appid = config.appid
    oauth2_refresh_url = wxconfig.oauth2_access_token_refresh_url.format(appid, refresh_token)
    http_client = AsyncHTTPClient()
    response = yield http_client.fetch(oauth2_refresh_url)
    logging.debug(response.body.decode())
    return json.loads(response.body.decode())


@gen.coroutine
def validate_oauth2_access_code(web_access_token, openid):
    if refresh_access_token or openid:
        return '{}'

    validate_url = wxconfig.validate_oauth2_access_token_url.format(web_access_token, openid)
    http_client = AsyncHTTPClient()
    response = yield http_client.fetch(validate_url)
    logging.debug(response.body.decode())
    return json.loads(response.body.decode())


@gen.coroutine
def pull_user_info(openid, web_access_token=None):
    if web_access_token:
        pull_user_info_url = wxconfig.pull_user_info_url.format(web_access_token, openid)
        http_client = AsyncHTTPClient()
        response = yield http_client.fetch(pull_user_info_url)
        logging.debug(response.body.decode())
        user_dict = json.loads(response.body.decode())
        user = dict_to_model(User, user_dict, ignore_unknown=True)
    else:
        user = User(openid='openid')

    user_id = None
    try:
        _user = DBUtil.do(User.get, User.openid == openid)
        user_id = _user.get_id()
        exists = True
    except DoesNotExist:
        exists = False

    if exists:
        assert user_id
        user.set_id(user_id)
        user.updatetime = datetime.datetime.now()
    else:
        user.createtime = datetime.datetime.now()
    yield DBUtil.do(user.save)
    user = yield DBUtil.do(User.get, User.openid == openid)

    return model_to_dict(user)


@gen.coroutine
def download_temp_resource(media_id, path=None):
    config = yield DBUtil.do(Config.get)
    url = wxconfig.temp_resource_download_url.format(config.accesstoken, media_id)
    http_client = AsyncHTTPClient()
    response = yield http_client.fetch(url)
    logging.debug(response.headers['Content-disposition'])
    logging.debug(response.headers['Date'])
    filename = response.headers['Content-disposition'][len('attachment; filename="'):-1]
    logging.debug(filename)
    if path is None:
        with open(filename, mode='wb') as file:
            file.write(response.body)
    else:
        if path[-1] != os.path.sep:
            path += os.path.sep
        with open(path + filename, mode='wb') as file:
            file.write(response.body)
