"""test wx_workers"""
import sys
sys.path.append("/home/gupengxiang/wx_third_part_platform")
# 地址测试的话需更换为实际目录地址
import unittest
from unittest import mock

from lib import wx_workers, wx_service

global APPID
APPID = ''


class TestProducer(unittest.TestCase):
    def setUp(self):
        global APPID
        APPID = APPID or "APPID"
        self.aaa = wx_workers.TEST_ZYClient(APPID)

    @mock.patch("dao.wx_service.get_user_base_info")
    @mock.patch.object(wx_service.WeChat_OAP, "send_template_msg")
    def test_medical_matter(self, mock_send_template_msg, mock_get_user_base_info):
        mock_send_template_msg.return_value = {"status": 0, "msg": "successbymock"}
        mock_get_user_base_info.return_value = {"openid": "by_mock"}
        data = {"Event": "SCAN", "FromUserName": "let's go!", "EventKey": "wys_1"}
        result = {"sign": 1, "msg": ''}
        self.assertEqual(self.aaa.medical_matter(data), result)

    @mock.patch("helper.api.get_aiw_push_info")
    @mock.patch.object(wx_service.WeChat_OAP, "send_template_msg")
    def test_aal_izz_well(self, mock_send_template_msg, mock_get_aiw_push_info):
        mock_send_template_msg.return_value = {"status": 0, "msg": "successbymock"}
        mock_get_aiw_push_info.return_value = {
            "status": 0,
            "url": "https://www.zuoshouyisheng.com/",
            "miniprogram": {  # 跳转小程序设定
                "appid": "wxacd37ff25cd2ed6a",
                "pagepath": "/pages/alarm/dose/index"
            },
            "data": {
                "first": {
                    "value": "恭喜你购买成功！",
                    "color": "#173177"
                },
                "keyword1": {
                    "value": "巧克力",
                    "color": "#173177"
                },
                "keyword2": {
                    "value": "39.8元",
                    "color": "#173177"
                },
                "keyword3": {
                    "value": "2014年9月22日",
                    "color": "#173177"
                },
                "remark": {
                    "value": "欢迎再次购买！",
                    "color": "#173177"
                }
            }
        }
        data = {
            "Event": "TEST",
            "FromUserName": "let's go!",
            "EventKey": "AIW_demo_%7B%7D",
            "real_event_key": "AIW&demo&%7B%7D",
            "real_event_key": 'AIW&demo&{"asd": 123}'
        }
        result = {"sign": 1, "msg": 'successbymock'}
        self.assertEqual(self.aaa.aal_izz_well(data), result)


if __name__ == '__main__':
    if len(sys.argv) == 2:
        APPID = sys.argv[1]
        del sys.argv[1]
    unittest.main()

