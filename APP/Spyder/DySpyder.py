"""
@Time    : 2023/4/5 12:05
@Author  : superhero
@Email   : 838210720@qq.com
@File    : demo.py
@IDE: PyCharm
"""
import hashlib
import re
import requests
import time
import urllib.parse
import json

from bs4 import BeautifulSoup

from APP.Spyder.makeRealURL import MakeRealURL

makeRealURL = MakeRealURL()


class DouYinSpyder():
    def __init__(self):
        self.user_url = "https://www.douyin.com/user/MS4wLjABAAAAfjsAJZbhlKTAhClTsxbP1b04RvyTjBRPgNWzLGnMR0c"
        # self.note_url = "https://www.douyin.com/video/7218888878109904186"
        # self.note_url = "https://www.douyin.com/user/MS4wLjABAAAASZj6di2175kheLW0qkCaaJSVzm3DjJqY9gpAv3DB5X3vtdA7AjAcls94-VVa3uIv?modal_id=7302669308935638309"
        self.note_url = "https://www.douyin.com/video/7258577937904012579"
        self.headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)'
                          'Chrome/111.0.0.0 Safari/537.36',
        }

    def set_sign(self):
        """
        计算api签名
        :return:
        """
        ts = str(time.time()).split('.')[0]
        string = '1005d9ba8ae07d955b83c3b04280f3dc5a4a' + ts + self.get_appkey()
        sign = hashlib.md5(string.encode('utf8')).hexdigest()
        return sign

    def get_appkey(self):
        """
        获取appkey
        :return:
        """
        data = 'd9ba8ae07d955b83c3b04280f3dc5a4a5c6b8r9a'
        return hashlib.sha256(data.encode('utf-8')).hexdigest()

    def getNoteInfo(self, token, url=""):
        self.headers['cookie'] = token
        url = url if url else self.note_url
        modal_id = makeRealURL.makeDYContent_id(url)
        if not modal_id:
            return {"status": "0", "message": "请输入正确的抖音笔记链接"}
        Referer = "https://www.douyin.com/video/" + modal_id
        spyder_url = "https://www.douyin.com/aweme/v1/web/aweme/detail/?"
        self.headers['Referer'] = Referer
        data = {
            "device_platform": "webapp",
            "aid": "6383",
            "channel": "channel_pc_web",
            "aweme_id": modal_id,
            "pc_client_type": "1",
            "version_code": "190500",
            "version_name": "19.5.0",
            "cookie_enabled": "true",
            "screen_width": "1920",
            "screen_height": "1080",
            "browser_language": "zh-CN",
            "browser_platform": "Win32",
            "browser_name": "Chrome",
            "browser_version": "114.0.0.0",
            "browser_online": "true",
            "engine_name": "Blink",
            "engine_version": "114.0.0.0",
            "os_name": "Windows",
            "os_version": "10",
            "cpu_core_num": "16",
            "device_memory": "8",
            "platform": "PC",
            "downlink": "10",
            "effective_type": "4g",
            "round_trip_time": "50",
            "webid": "7303072417411532314",
            "msToken": "rCasLwylPrkYXfqOpkyoV47dPbeOH9ezXdKrnkuR5rWZSe1ld4kjkZHD8xbobObGm-hraDQvOSJLZtEMwM_hr4NnGGQbqGg1jsBOin0-xQ6Ku4-9MgfagAHmZK8=",
        }
        spyder_url = spyder_url + urllib.parse.urlencode(data)
        response = requests.get(spyder_url, headers=self.headers)
        if response.status_code == 200:
            notice = self.testNotice(response)
            if notice:
                data = response.json()['aweme_detail']
                if data:
                    upload_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(data.get("create_time")))
                    account_id = data.get("author").get('sec_uid')
                    title_result = {
                        "title": data.get("desc"),
                        "content_id": modal_id,
                        "liked": data.get("statistics").get("digg_count"),
                        "desc": data.get("statistics").get("desc"),
                        "collected": data.get("statistics").get("collect_count"),
                        "commented": data.get("statistics").get("comment_count"),
                        "forwarded": data.get("statistics").get("share_count"),
                        "imageList": [],
                        "commentList": [],
                        "hashTags": [],
                        "video_link": url,
                        "spyder_url": url,
                        "upload_time": upload_time,
                        "content_link": "",
                        "status": "正常",
                        "account_id": account_id,
                        "profile_link": "https://www.douyin.com/user/" + account_id,

                    }
                    return {"status": "1", "message": title_result}
                else:
                    return {"status": "3", "message": "笔记不存在"}
            else:
                return {"status": "3", "message": "笔记不存在"}
        else:
            return {"status": "2", "message": "登录已过期"}

    def testCookie(self, token):
        result = self.getNoteInfo(token=token)
        if result.get("status") == "1" or result.get("status") == "3":
            return {'status': 'success', 'message': "抖音测试成功"}
        else:
            return result

    def testNotice(self, response):
        try:
            notice = response.json()['filter_detail']['notice']
            if notice == "抱歉，作品不见了":
                return False
            else:
                return True
        except:
            return True

    def getUserInfo(self, token, url=""):
        self.headers['cookie'] = token
        url = url if url else self.user_url
        modal_id = makeRealURL.makeDYAccount_id(url)
        if not modal_id:
            return {"status": "0", "message": "请输入正确的抖音笔记链接"}
        # Referer = "https://www.douyin.com/user/MS4wLjABAAAAfjsAJZbhlKTAhClTsxbP1b04RvyTjBRPgNWzLGnMR0c" + modal_id
        Referer = "https://www.douyin.com/user/MS4wLjABAAAAfjsAJZbhlKTAhClTsxbP1b04RvyTjBRPgNWzLGnMR0c"
        spyder_url = "https://www.douyin.com/aweme/v1/web/user/profile/other/?"
        self.headers['Referer'] = Referer
        self.headers['Accept'] = "application/json, text/plain, */*"
        print(self.headers)
        print(spyder_url)
        data = {
            "device_platform": "webapp",
            "aid": "6383",
            "channel": "channel_pc_web",
            "publish_video_strategy_type": "2",
            "source": "channel_pc_web",
            "sec_user_id": "MS4wLjABAAAAfjsAJZbhlKTAhClTsxbP1b04RvyTjBRPgNWzLGnMR0c",
            "personal_center_strategy": "1",
            "pc_client_type": "1",
            "version_code": "170400",
            "version_name": "17.4.0",
            "cookie_enabled": "true",
            "screen_width": "1920",
            "screen_height": "1080",
            "browser_language": "zh-CN",
            "browser_platform": "Win32",
            "browser_name": "Chrome",
            "browser_version": "114.0.0.0",
            "browser_online": "true",
            "engine_name": "Blink",
            "engine_version": "114.0.0.0",
            "os_name": "Windows",
            "os_version": "10",
            "cpu_core_num": "16",
            "device_memory": "8",
            "platform": "PC",
            "downlink": "10",
            "effective_type": "4g",
            "round_trip_time": "50",
            "webid": "7303072417411532314",
            "msToken": "zVVXyjH-xhkfnivZIFYrDxlrz_1mN470OCWcsOx6nJRP18nt4FnQP-cTF6NYZ8M06I1xVxAv0ggG7cuAewNj53zejYhE00bKJzdMltrdczZTlsWraYmx2d1ntVMn",
            "X-Bogus": "DFSzswVOJTxANJ8btzwanRXAIQRX",

        }
        spyder_url = spyder_url + urllib.parse.urlencode(data)
        response = requests.get(spyder_url, headers=self.headers)
        print(spyder_url)
        print(response.content)
        # Account_result = {
        #     "nickname": soup.select('div.HqxPzh_q')[0].text if soup.select('div.HqxPzh_q') else "",
        #     "follow": int(self.changeNumber(soup.select('div.TxoC9G6_')[0].text)) if soup.select(
        #         'div.TxoC9G6_') else 0,
        #     "fans": int(self.changeNumber(soup.select('div.TxoC9G6_')[1].text)) if soup.select(
        #         'div.TxoC9G6_') else 0,
        #     "gender": None,
        #     "liked": int(self.changeNumber(soup.select('div.TxoC9G6_')[2].text)) if soup.select(
        #         'div.TxoC9G6_') else 0,
        #     "account_id": soup.select('span.aH7rLkZZ')[0].text if soup.select('span.aH7rLkZZ') else "",
        #     "notes": int(soup.select('span.J6IbfgzH')[0].text) if soup.select('span.J6IbfgzH') else 0,
        #     "boards": None,
        #     "location": soup.select('span.a83NyFJ4')[0].text if soup.select('span.a83NyFJ4') else "",
        #     "collected": None,
        #     "desc": "".join([span.text for span in soup.select('span.Nu66P_ba')]) if soup.select(
        #         'span.Nu66P_ba') else "",
        #     "officialVerifyName": soup.select('div.HqxPzh_q')[0].text if soup.select('div.HqxPzh_q') else "",
        #     "profile_link": url,
        #     "spyder_url": url,
        #     "status": "正常",
        # }
        # if Account_result["nickname"] != "":
        #     return {'status': '1', 'message': Account_result}
        # else:
        #     return {"status": "2", "message": "获取抖音数据出错"}
        # else:
        #     return {"status": "2", "message": "token已过期"}

    def changeNumber(self, number_str):
        if "万" in number_str:
            number_str = number_str.replace("万", "")
        return str(int(float(number_str) * 10000))


if __name__ == '__main__':
    dy = DouYinSpyder()
    token = 'ttwid=1%7CR2iz-zprlt6A_O_khmqi8WvZnjvk2N6PiLASc8ylM-M%7C1700379066%7Cc43b6114c76844ded9fda67b74147db0d47d0f138ffbcd0c848ba4a2967f537e; passport_csrf_token=ca6a2160323aeaf35c20b9f5fde86c72; passport_csrf_token_default=ca6a2160323aeaf35c20b9f5fde86c72; volume_info=%7B%22isUserMute%22%3Afalse%2C%22isMute%22%3Atrue%2C%22volume%22%3A0.6%7D; s_v_web_id=verify_lp55smva_Ka8sAsmh_6qv0_4b6Q_9NJb_hoOPANDLjfUu; xgplayer_user_id=446687971665; FORCE_LOGIN=%7B%22videoConsumedRemainSeconds%22%3A180%2C%22isForcePopClose%22%3A1%7D; ttcid=d16be550844342098cd89f74ad40bbea39; d_ticket=e31c32687fe00ad6ef78aacc6851ae7847f36; passport_assist_user=Cjy0UMXqiuSuHoNhhEDJTBVl6P_Ll_SKaX3u8v6Dzm687v17XpmjtHCaY0XNtX7YDbIYNmE78AJobioV9WgaSgo8YwjZ4DYp8vG5XB8t1UGX-0YcOKxXqxllKluu1fFaE_7kaLbY7JuxD43C2wSHWTF5C3mkl32Aduh5qe5VELDawQ0Yia_WVCABIgEDcJa8uQ%3D%3D; n_mh=acm93QdnGeokQ8P9OssEFwOxgViwjjf-3wI379AUXj0; sso_auth_status=415d996fd54f2d69d901663620746fe8; sso_auth_status_ss=415d996fd54f2d69d901663620746fe8; sso_uid_tt=c58f1e24c0e9d635f00f5b1fb362a7ae; sso_uid_tt_ss=c58f1e24c0e9d635f00f5b1fb362a7ae; toutiao_sso_user=5c32092d523ddecdb2a825e60882716b; toutiao_sso_user_ss=5c32092d523ddecdb2a825e60882716b; sid_ucp_sso_v1=1.0.0-KDAzZWFmMzUxNjk1MTI4Nzg3N2ExZGQ4ODk1OTI2ZjY0NWM2MDc3YmIKHQjAgNWO4wIQzfPmqgYY7zEgDDDy4aHVBTgCQPEHGgJobCIgNWMzMjA5MmQ1MjNkZGVjZGIyYTgyNWU2MDg4MjcxNmI; ssid_ucp_sso_v1=1.0.0-KDAzZWFmMzUxNjk1MTI4Nzg3N2ExZGQ4ODk1OTI2ZjY0NWM2MDc3YmIKHQjAgNWO4wIQzfPmqgYY7zEgDDDy4aHVBTgCQPEHGgJobCIgNWMzMjA5MmQ1MjNkZGVjZGIyYTgyNWU2MDg4MjcxNmI; passport_auth_status=161f7fd86fbb82595e8a0c1b78f6a51c%2C6a8c773765bc1cefd5397baa5a1055c5; passport_auth_status_ss=161f7fd86fbb82595e8a0c1b78f6a51c%2C6a8c773765bc1cefd5397baa5a1055c5; sid_ucp_v1=1.0.0-KGNmZTVlNDZjMDI2MDViOGQxMDRiZGZhNDA3NGI3YmRmNTIzMmQxYTMKGQjAgNWO4wIQzvPmqgYY7zEgDDgCQPEHSAQaAmxxIiBhYTI4YzkwNjFhYTUwNGI2YmI3NzZhMzhjNjQwZmRkNQ; ssid_ucp_v1=1.0.0-KGNmZTVlNDZjMDI2MDViOGQxMDRiZGZhNDA3NGI3YmRmNTIzMmQxYTMKGQjAgNWO4wIQzvPmqgYY7zEgDDgCQPEHSAQaAmxxIiBhYTI4YzkwNjFhYTUwNGI2YmI3NzZhMzhjNjQwZmRkNQ; sid_guard=5c32092d523ddecdb2a825e60882716b%7C1700379086%7C5184001%7CThu%2C+18-Jan-2024+07%3A31%3A27+GMT; uid_tt=c58f1e24c0e9d635f00f5b1fb362a7ae; uid_tt_ss=c58f1e24c0e9d635f00f5b1fb362a7ae; sid_tt=5c32092d523ddecdb2a825e60882716b; sessionid=5c32092d523ddecdb2a825e60882716b; sessionid_ss=5c32092d523ddecdb2a825e60882716b; LOGIN_STATUS=1; publish_badge_show_info=%220%2C0%2C0%2C1700379097310%22; _bd_ticket_crypt_doamin=2; _bd_ticket_crypt_cookie=3d0d05b6ef426481638a8e4dfb572324; __security_server_data_status=1; store-region=cn-gd; store-region-src=uid; download_guide=%223%2F20231119%2F0%22; pwa2=%220%7C0%7C3%7C0%22; VIDEO_FILTER_MEMO_SELECT=%7B%22expireTime%22%3A1701083705243%2C%22type%22%3A1%7D; stream_player_status_params=%22%7B%5C%22is_auto_play%5C%22%3A0%2C%5C%22is_full_screen%5C%22%3A0%2C%5C%22is_full_webscreen%5C%22%3A0%2C%5C%22is_mute%5C%22%3A1%2C%5C%22is_speed%5C%22%3A1%2C%5C%22is_visible%5C%22%3A0%7D%22; dy_swidth=1920; dy_sheight=1080; strategyABtestKey=%221700802011.049%22; bd_ticket_guard_client_web_domain=2; csrf_session_id=a35196123462965bb07c7763a777f3c7; FOLLOW_NUMBER_YELLOW_POINT_INFO=%22MS4wLjABAAAA9Ax-pVKjsUPUNdV-gbVq5OBjCe9HrIGwrNnNrTUP6pQ%2F1700841600000%2F0%2F0%2F1700818725594%22; __ac_nonce=065607ee900ca2e1d9007; __ac_signature=_02B4Z6wo00f01-XWkxQAAIDChtxTfglGWJPl9peAAJwfNwYY2QEFOio3CailbYg59h6viNTvX1x-yUkoXKnPAWYhB05Cd2n-fk.FkBW2kDm7uViaS.gvPm0RVOL4P6vuYBClJ2O0WvBEqPrXfe; msToken=huLUB-XSxazA5Acrmvw9s17HL31Vn6J3BSHIUq_Erd_ijl_fNHGDNL9HKhDU6cKmS9Zgge15aY0VghcqK0ftppzEXv2U6Z15BZwpPsnEW6SQooyIezvMjzf0Ss7f; tt_scid=AF0W-D.qVNDuFq.BOSQxjUfY.SiRjmV8zOIs8JdKGR4D46DJ8SFcwEN.lcE-wbdp8ee9; odin_tt=a30b313c100e0ffa3075443f9e901dcf1344ff42a87dce72ac13714964724de0d50ac8ce2af0899c9be8babc0883b646; msToken=braWAzgTHzXaVwxbq1pdq1Y8o92nqEse6N_P-ytUz7PIzVWw5Wya_Hn-AbVKGzNmM7fGU9As3ZekQDergWAw6rACi5LdFNa0WJVhuiYdflq7W23Ile6Gkpe8OgD0; passport_fe_beating_status=false; stream_recommend_feed_params=%22%7B%5C%22cookie_enabled%5C%22%3Atrue%2C%5C%22screen_width%5C%22%3A1920%2C%5C%22screen_height%5C%22%3A1080%2C%5C%22browser_online%5C%22%3Atrue%2C%5C%22cpu_core_num%5C%22%3A16%2C%5C%22device_memory%5C%22%3A8%2C%5C%22downlink%5C%22%3A10%2C%5C%22effective_type%5C%22%3A%5C%224g%5C%22%2C%5C%22round_trip_time%5C%22%3A0%7D%22; IsDouyinActive=true; FOLLOW_LIVE_POINT_INFO=%22MS4wLjABAAAA9Ax-pVKjsUPUNdV-gbVq5OBjCe9HrIGwrNnNrTUP6pQ%2F1700841600000%2F0%2F1700823955448%2F0%22; home_can_add_dy_2_desktop=%221%22; bd_ticket_guard_client_data=eyJiZC10aWNrZXQtZ3VhcmQtdmVyc2lvbiI6MiwiYmQtdGlja2V0LWd1YXJkLWl0ZXJhdGlvbi12ZXJzaW9uIjoxLCJiZC10aWNrZXQtZ3VhcmQtcmVlLXB1YmxpYy1rZXkiOiJCQTRaOFJWNi9ORnZRSmxPT3hXMGpOeFYzQUcwcTNwcG5aSWkwZ2xoYWFTd0kwcSs4ZUloc0hwMm92eEJCdEpFT2szaGd0aDlKaVcvV3N2bHMydTg1Yzg9IiwiYmQtdGlja2V0LWd1YXJkLXdlYi12ZXJzaW9uIjoxfQ%3D%3D'
    result = dy.getUserInfo(token=token)
    # result = dy.getNoteInfo(token=token)
    print(result)
