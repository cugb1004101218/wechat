# -*- coding: utf-8 -*-
import hashlib
import requests
import datetime

class WechatAPI(object):
    def __init__(self, appid, secret, token):
        self.appid = appid
        self.secret = secret
        self.token = token
        self.last_get_access_token_time = datetime.datetime.strptime("1970-01-01 00:00:00", "%Y-%m-%d %H:%M:%S")
        self.access_token = None

    # 验证服务器
    def check_signature(self, signature, timestamp, nonce):
        pwd = "".join(sorted([self.token, timestamp, nonce]))
        return hashlib.sha1(pwd).hexdigest() == signature

    # 获取access_token
    def get_access_token(self):
        now_time = datetime.datetime.now()
        # 6000 秒之内直接取上次获取的结果
        if now_time - self.last_get_access_token_time < datetime.timedelta(seconds=6000) and self.access_token:
            return self.access_token
        r = requests.get("https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid=" + self.appid + "&secret=" + self.secret)
        ret = r.json()
        self.access_token = ret.get("access_token", None)
        self.last_get_access_token_time = now_time
        return self.access_token
