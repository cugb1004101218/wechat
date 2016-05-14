# -*- coding: utf-8 -*-
import datetime
import time
import tornado.ioloop
import tornado.httpserver
import tornado.web
from tornado.options import define, options
import sys
sys.path.append('..')

from wechat_api.message import *

import ConfigParser
from wechat_api.api import *
config = ConfigParser.ConfigParser()
config.read('../wechat.config')
appid = config.get("base_info", "appid")
secret = config.get("base_info", "secret")
token = config.get("base_info", "token")

wc_api = WechatAPI(appid, secret, token)

define("port", default=80, help="run on the given port", type=int)
define("ip", default="0.0.0.0", help="server_ip", type=str)

class WechatHandler(tornado.web.RequestHandler):
    # 具体需求你们可以继承 WechatHandler 这个类
    def initialize(self, wechat_api):
        self.wechat_api = wechat_api

    def get(self):
        self.check_wechat_server()

    # 直接返回用户的文本消息
    def post(self):
        xml_str = self.request.body
        text_msg = TextMessage()
        text_msg.parse_from_xml(xml_str)
        reply_msg = TextMessage()
        reply_msg.to_user_name = text_msg.from_user_name
        reply_msg.from_user_name = text_msg.to_user_name
        reply_msg.content = text_msg.content
        self.reply(reply_msg)

    # 验证微信服务器
    def check_wechat_server(self):
        signature = self.get_argument('signature')
        nonce = self.get_argument('nonce')
        timestamp = self.get_argument('timestamp')
        echostr = self.get_argument('echostr')
        if self.wechat_api.check_signature(signature, timestamp, nonce):
            self.write(echostr)

    def reply(self, msg):
        msg.create_timestamp = int(time.time())
        self.write(msg.to_xml_str())

application = tornado.web.Application([
    (r"/", WechatHandler, dict(wechat_api=wc_api)),
], debug=True)

if __name__ == "__main__":
    http_server = tornado.httpserver.HTTPServer(application, xheaders=True)
    http_server.listen(options.port, address=options.ip)
    tornado.ioloop.IOLoop.instance().start()
