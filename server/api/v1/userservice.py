#! /usr/bin/env python3.5
# coding: utf-8

import json
import logging

from peewee import DoesNotExist
from playhouse import shortcuts
from tornado import gen

from api.postonlyhandler import PostOnlyHandler
from api.response import Response
from model import dbutil
from model.user import User


class GetUserInfoHandler(PostOnlyHandler):
    @gen.coroutine
    def post(self):
        openid = None
        try:
            request = json.loads(self.request.body.decode())
            openid = request['openid']
            logging.debug('openid: {0}'.format(openid))
            user = yield dbutil.do(User.select().where(User.openid == openid).get)
            self.write(Response(
                status=1, msg='ok',
                result=shortcuts.model_to_dict(user)
            ).json())
        except DoesNotExist as e:
            self.write(Response(msg='sorry，亲，用户不存在 openid={0}'.format(openid)).json())
            logging.exception('GetUserInfoHandler error: {0}'.format(str(e)))
        except Exception as e:
            self.write(Response(msg='sorry，亲，查询用户失败 openid={0}'.format(openid)).json())
            logging.exception('GetUserInfoHandler error: {0}'.format(str(e)))


class UpdateUserInfoHandler(PostOnlyHandler):
    @gen.coroutine
    def post(self):
        openid = None
        try:
            request = json.loads(self.request.body.decode())
            id = request.get('id', None)
            openid = request.get('openid', None)
            if openid is None:
                raise AttributeError
            if id is None:
                user = yield dbutil.do(User.select(User.id).where(User.openid == openid).get)
                id = user.get_id()
            modified_user = shortcuts.dict_to_model(User, request, ignore_unknown=True)
            modified_user.set_id(id)
            yield dbutil.do(modified_user.save)
            self.write(Response(
                status=1, msg='ok',
                result={}
            ).json())
        except AttributeError as e:
            self.write(Response(msg='sorry，亲，修改用户信息时必须包含openid').json())
            logging.exception('UpdateUserInfoHandler error: {0}'.format(str(e)))
        except DoesNotExist as e:
            self.write(Response(msg='sorry，亲，用户不存在 openid={0}'.format(openid)).json())
            logging.exception('UpdateUserInfoHandler error: {0}'.format(str(e)))
        except Exception as e:
            self.write(Response(msg='sorry，亲，修改用户信息失败').json())
            logging.exception('UpdateUserInfoHandler error: {0}'.format(str(e)))
