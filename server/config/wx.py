#! /usr/bin/env python3.5
# coding: utf-8

access_token_url = 'https://api.weixin.qq.com/cgi-bin/token' + \
                   '?grant_type=client_credential&appid={0}&secret={1}'
oauth2_access_token_url = 'https://api.weixin.qq.com/sns/oauth2/access_token' + \
                          '?appid={0}&secret={1}&code={2}&grant_type=authorization_code'
oauth2_access_token_refresh_url = 'https://api.weixin.qq.com/sns/oauth2/refresh_token' + \
                                  '?appid={0}&grant_type=refresh_token&refresh_token={1}'
validate_oauth2_access_token_url = 'https://api.weixin.qq.com/sns/auth' + \
                                   '?access_token={0}&openid={1}'
jsapi_ticket_url = 'https://api.weixin.qq.com/cgi-bin/ticket/getticket' + \
                   '?access_token={0}&type=jsapi'
pull_user_info_url = 'https://api.weixin.qq.com/sns/userinfo?' + \
                     'access_token={0}&openid={1}&lang=zh_CN'
get_user_info_url = 'https://api.weixin.qq.com/cgi-bin/user/info?' + \
                    'access_token={0}&openid={1}&lang=zh_CN'
custom_msg_url = 'https://api.weixin.qq.com/cgi-bin/message/custom/send?access_token={0}'
temp_resource_download_url = 'http://api.weixin.qq.com/cgi-bin/media/get?access_token={0}&media_id={1}'
temp_resource_upload_url = 'http://api.weixin.qq.com/cgi-bin/media/upload?access_token={0}&type={1}'
temp_qrcode_url = 'https://api.weixin.qq.com/cgi-bin/qrcode/create?access_token={0}'
temp_qrcode_ticket_url = 'https://mp.weixin.qq.com/cgi-bin/showqrcode?ticket={0}'
success_response = 'success'
error_response = ''
custom_text_template = {'touser': None, 'msgtype': 'text', 'text': {'content': None}}
