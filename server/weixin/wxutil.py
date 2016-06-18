#! /usr/bin/env python3.5
# coding: utf-8

import copy
import datetime
import json
import logging
import os
import sys
import time
from ftplib import FTP

from peewee import DoesNotExist
from playhouse.shortcuts import dict_to_model, model_to_dict
from tornado import escape
from tornado import gen
from tornado.httpclient import AsyncHTTPClient

from config import sync as syncconfig
from config import wx as wxconfig
from model import dbutil
from model.config import Config
from model.templatemsg import Templatemsg
from model.user import User

logger = logging.getLogger(__name__)

@gen.coroutine
def refresh_access_token():
    logging.info('开始刷新微信access token')
    try:
        config = yield dbutil.do(Config.select().get)
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
        yield dbutil.do(config.save)
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
    config = yield dbutil.do(Config.get)
    return config.accesstoken


@gen.coroutine
def get_jsapi_ticket():
    config = yield dbutil.do(Config.get)
    return config.jsapiticket


@gen.coroutine
def send_template_msg(templatemsg):
    if templatemsg is None: return
    logging.info('wxutil.send_template_msg - 发送模板消息：{0}'.format(templatemsg))
    config = yield dbutil.do(Config.get)
    url = wxconfig.custom_msg_url.format(config.accesstoken)
    # data = {
    #     'touser': templatemsg.touser,
    #     'template_id': templatemsg.templateid,
    #     'url': templatemsg.url,
    #     'data': json.loads(templatemsg.data)
    # }
    http_client = AsyncHTTPClient()
    response = yield http_client.fetch(url, **{'method': 'POST',
                                               'body': json.dumps(templatemsg, ensure_ascii=False)})
    result = json.loads(response.body.decode())
    errcode = result['errcode']
    if errcode == 0:
        templatemsg['msgid'] = result['msgid']
        templatemsg['updatetime'] = datetime.datetime.now()
        tmsg = dict_to_model(Templatemsg, templatemsg)
        yield dbutil.do(tmsg.save)
    else:
        raise RuntimeError('wxutil.send_template_msg-发送模板消息失败，消息内容：{0}'.format(templatemsg))


@gen.coroutine
def send_custom_msg(msg, reply):
    custom_text = copy.deepcopy(wxconfig.custom_text_template)
    custom_text['touser'] = msg.fromusername
    custom_text['text']['content'] = reply
    logging.debug(custom_text)

    config = yield dbutil.do(Config.select().get)
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

    config = dbutil.do(Config.get)
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

    config = dbutil.do(Config.get)
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
        _user = dbutil.do(User.get, User.openid == openid)
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
    yield dbutil.do(user.save)
    user = yield dbutil.do(User.get, User.openid == openid)
    return model_to_dict(user)


@gen.coroutine
def get_user_info(openid):
    id = None
    try:
        _user = yield dbutil.do(User.get, User.openid == openid)
        id = _user.get_id()
    except DoesNotExist:
        pass
    access_token = yield get_access_token()
    get_user_info_url = wxconfig.get_user_info_url.format(access_token, openid)
    http_client = AsyncHTTPClient()
    response = yield http_client.fetch(get_user_info_url)
    result = json.loads(response.body.decode())
    logging.debug(result)
    try:
        # 未关注微信号时，会出错
        result['errcode']
    except Exception:
        user = dict_to_model(User, result, ignore_unknown=True)
        if id:
            user.set_id(id)
        # yield dbutil.do(user.save)
        return model_to_dict(user)
    logging.error('拉取用户信息出错：{0}'.format(result))

@gen.coroutine
def process_temp_resource(media_id):
    try:
        logging.info('开始下载media文件:' + media_id)
        file_info = yield download_temp_resource(media_id)
        path, filename = file_info['path'], file_info['filename']
        logging.info('写入本地文件: {0}'.format(path + filename))
        logging.info('media文件: {0} 下载完成'.format(media_id))
        logging.info('开始上传media文件到OSS: ' + filename)
        url = yield upload_temp_resource(path, filename)
        logging.info('media文件: {0} 上传完毕，URL为{1}'.format(filename, url))
        os.remove(path + filename)
        logging.info('删除本地文件: {0}'.format(path + filename))
        return url
    except Exception as e:
        logging.exception('wxutil.download_temp_resource media_id:{0} error: {1}'.format(media_id, str(e)))
        return None


@gen.coroutine
def download_temp_resource(media_id):
    config = yield dbutil.do(Config.get)
    url = wxconfig.temp_resource_download_url.format(config.accesstoken, media_id)
    http_client = AsyncHTTPClient()
    response = yield http_client.fetch(url)
    filename = response.headers['Content-disposition'][len('attachment; filename="'):-1]
    if syncconfig.store_at:
        path = syncconfig.store_at
    else:
        path = sys.path[0] + os.path.sep + syncconfig.default_name
    os.makedirs(path, exist_ok=True)
    if path[-1] != os.path.sep:
        path += os.path.sep
    with open(path + filename, mode='wb') as file:
        file.write(response.body)
    return {'path': path, 'filename': filename}


@gen.coroutine
def upload_temp_resource(path, filename):
    ftp = FTP()
    ftp.connect(syncconfig.ftp_server, syncconfig.ftp_port)
    ftp.login(syncconfig.ftp_user, syncconfig.ftp_password)
    remote_path = '/'.join([
        time.strftime('%Y'),
        time.strftime('%m'),
        time.strftime('%d')
    ])
    ftp.mkd(remote_path)
    with open(path + filename, 'rb') as file:
        ftp.storbinary('STOR ' + remote_path + '/' + filename, file)
    return syncconfig.url_prefix + remote_path + '/' + filename


@gen.coroutine
def get_temp_qrcode_url(event_id):
    access_token = yield get_access_token()
    url = wxconfig.temp_qrcode_url.format(access_token)
    param = {
        'expire_seconds': 2592000,
        'action_name': 'QR_SCENE',
        'action_info': {
            'scene': {
                'scene_id': event_id
            }
        }
    }
    http_client = AsyncHTTPClient()
    response = yield http_client.fetch(url, **{'method': 'POST',
                                               'body': json.dumps(param, ensure_ascii=False)})
    result = json.loads(response.body.decode())
    ticket = escape.url_escape(result['ticket'])
    return wxconfig.temp_qrcode_ticket_url.format(ticket)
