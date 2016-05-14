# -*- coding: utf-8 -*-
from xml.etree import ElementTree

class MessageType:
    kText = 0
    kImage = 1
    kVoice = 2
    kVideo = 3
    kShortVideo = 4
    kLocation = 5
    kLink = 6

msg_type_map = {
    "text": MessageType.kText,
    "image": MessageType.kImage,
    "voice": MessageType.kVoice,
    "video": MessageType.kVideo,
    "shortvideo": MessageType.kShortVideo,
    "location": MessageType.kLocation,
    "link": MessageType.kLink,
}

class BaseMessage(object):
    def __init__(self,
                 to_user_name=None,
                 from_user_name=None,
                 create_timestamp=None,
                 msg_type=None,
                 msg_id=None):

        self.to_user_name = to_user_name
        self.from_user_name = from_user_name
        self.create_timestamp = create_timestamp
        self.msg_type = msg_type
        self.msg_id = msg_id
        self.xml_root = None

    def parse_from_xml(self, xml_str):
        root = ElementTree.fromstring(xml_str)
        self.xml_root = root
        self.to_user_name = root.find('ToUserName').text
        self.from_user_name = root.find('FromUserName').text
        self.create_timestamp = int(root.find('CreateTime').text)
        self.msg_type = msg_type_map[root.find('MsgType').text]
        self.msg_id = root.find('MsgId').text

class TextMessage(BaseMessage):
    def __init__(self,
                 to_user_name=None,
                 from_user_name=None,
                 create_timestamp=None,
                 msg_id=None,
                 content=None):
        super(TextMessage, self).__init__(to_user_name,
                                          from_user_name,
                                          create_timestamp,
                                          MessageType.kText,
                                          msg_id)
        self.content = content

    def parse_from_xml(self, xml_str):
        super(TextMessage, self).parse_from_xml(xml_str)
        self.content = self.xml_root.find('Content').text

    def to_xml_str(self):
        lines = []
        lines.append("<xml>")
        lines.append("<ToUserName><![CDATA[" + self.to_user_name + "]]></ToUserName>")
        lines.append("<FromUserName><![CDATA[" + self.from_user_name + "]]></FromUserName>")
        lines.append("<CreateTime>" + str(self.create_timestamp) + "</CreateTime>")
        lines.append("<MsgType><![CDATA[text]]></MsgType>")
        lines.append("<Content><![CDATA[" + self.content + "]]></Content>")
        lines.append("</xml>")
        return "\n".join(lines)
