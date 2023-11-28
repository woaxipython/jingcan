"""
@Time    : 2023/4/5 12:05
@Author  : superhero
@Email   : 838210720@qq.com
@File    : demo.py
@IDE: PyCharm
"""
import time

import requests
import urllib.parse
from APP.Spyder.makeDYInfo.makeInfo import get_profile_params, get_note_info, get_note_params, testNotice, \
    makeProfileSpyderURL, get_headers, get_profile_info, makeNotesSpyderURL, \
    get_user_note_info, makeSearchNoteSpyderURL, get_search_note_info
from APP.Spyder.makeRealURL import MakeRealURL

makeRealURL = MakeRealURL()


class DouYinSpyder():

    def __init__(self, info=None):
        self.user_url = "https://www.douyin.com/user/MS4wLjABAAAA-gF78FzT5spLYPC0Up91eT2Sc_v7XajjfzFwRZcC2ZU"
        self.note_url = "https://www.douyin.com/video/7258577937904012579"
        self.headers = get_headers()

    def testCookie(self, token, webid, msToken):
        # print(token, webid, msToken)
        result = self.getNoteInfo(token, webid, msToken)
        message = result.get("message")
        if isinstance(message, dict):
            title = message.get("title")
            return {'status': 'success', 'message': "成功，获取到标题：" + title}
        else:
            return result

    def getNoteInfo(self, token, webid, msToken, url=""):
        self.headers['cookie'] = token
        url = url if url else self.note_url
        modal_id = makeRealURL.makeDYContent_id(url)
        if not modal_id:
            return {"status": "0", "message": "请输入正确的抖音笔记链接"}
        Referer = "https://www.douyin.com/video/" + modal_id
        spyder_url = "https://www.douyin.com/aweme/v1/web/aweme/detail/?"
        self.headers['Referer'] = Referer
        data = get_note_params(webid, msToken, modal_id)
        spyder_url = spyder_url + urllib.parse.urlencode(data)
        response = requests.get(spyder_url, headers=self.headers)
        if not response.status_code == 200:
            return {"status": "2", "message": "登录已过期"}
        notice = testNotice(response)
        if isinstance(notice, str):
            return {"status": "3", "message": notice}
        data = response.json()
        if not data.get('aweme_detail'):
            return {"status": "3", "message": "笔记不存在"}
        # print(data.get('aweme_detail'))
        print("----------------------------")
        result = get_note_info(data.get('aweme_detail'), url, modal_id)
        return {"status": "1", "message": result}

    def getUserInfo(self, token, webid, msToken, url=""):
        self.headers['cookie'] = token
        url = url if url else self.user_url
        modal_id = makeRealURL.makeDYAccount_id(url)
        if not modal_id:
            return {"status": "0", "message": "请输入正确的抖音笔记链接"}
        spyder_url = makeProfileSpyderURL(webid, msToken, sec_user_id=modal_id)
        response = requests.get(spyder_url, headers=self.headers)
        if not response.status_code == 200:
            return {"status": "2", "message": "登录已过期"}
        print(response.json())
        data = response.json()['user']
        if not data:
            return {"status": "3", "message": "用户不存在"}
        result = get_profile_info(data, url, modal_id)
        return {"status": "1", "message": result}

    def getUserNoteList(self, token, webid, msToken, url="", max_cursor="0"):
        self.headers['cookie'] = token
        url = url if url else self.user_url
        sec_user_id = makeRealURL.makeDYAccount_id(url)
        if not sec_user_id:
            return {"status": "0", "message": "请输入正确的抖音笔记链接"}
        spyder_url = makeNotesSpyderURL(webid, msToken, sec_user_id, max_cursor)
        response = requests.get(spyder_url, headers=self.headers)
        if not response.status_code == 200 and not response.json()["aweme_list"]:
            return {"status": "2", "message": "登录已过期"}
        data = response.json()
        max_cursor = str(data['max_cursor'])
        hsa_more = data['has_more']
        for item in data['aweme_list']:
            result = get_user_note_info(item)
            yield {'status': '1', 'message': result, "max_cursor": max_cursor, "has_more": hsa_more}

    def getSearchNoteList(self, token, webid, msToken, keyword, sort_type="0", offset="0"):
        self.headers['cookie'] = token

        spyder_url = makeSearchNoteSpyderURL(webid, msToken, keyword, sort_type, offset)
        response = requests.get(spyder_url, headers=self.headers)
        if not response.status_code == 200 and not response.json():
            return {"status": "2", "message": "登录已过期"}
        data = response.json().get("data")
        if not data:
            return {"status": "2", "message": "登录已过期"}
        for item in data:
            if item.get("type") == 1 and item.get("aweme_info").get("desc"):
                # print(item)
                result = get_search_note_info(item["aweme_info"])
                yield {'status': '1', 'message': result}


if __name__ == '__main__':
    dy = DouYinSpyder()
    token = 'ttwid=1%7CR2iz-zprlt6A_O_khmqi8WvZnjvk2N6PiLASc8ylM-M%7C1700379066%7Cc43b6114c76844ded9fda67b74147db0d47d0f138ffbcd0c848ba4a2967f537e; passport_csrf_token=ca6a2160323aeaf35c20b9f5fde86c72; passport_csrf_token_default=ca6a2160323aeaf35c20b9f5fde86c72; volume_info=%7B%22isUserMute%22%3Afalse%2C%22isMute%22%3Atrue%2C%22volume%22%3A0.6%7D; s_v_web_id=verify_lp55smva_Ka8sAsmh_6qv0_4b6Q_9NJb_hoOPANDLjfUu; xgplayer_user_id=446687971665; FORCE_LOGIN=%7B%22videoConsumedRemainSeconds%22%3A180%2C%22isForcePopClose%22%3A1%7D; ttcid=d16be550844342098cd89f74ad40bbea39; d_ticket=e31c32687fe00ad6ef78aacc6851ae7847f36; passport_assist_user=Cjy0UMXqiuSuHoNhhEDJTBVl6P_Ll_SKaX3u8v6Dzm687v17XpmjtHCaY0XNtX7YDbIYNmE78AJobioV9WgaSgo8YwjZ4DYp8vG5XB8t1UGX-0YcOKxXqxllKluu1fFaE_7kaLbY7JuxD43C2wSHWTF5C3mkl32Aduh5qe5VELDawQ0Yia_WVCABIgEDcJa8uQ%3D%3D; n_mh=acm93QdnGeokQ8P9OssEFwOxgViwjjf-3wI379AUXj0; sso_auth_status=415d996fd54f2d69d901663620746fe8; sso_auth_status_ss=415d996fd54f2d69d901663620746fe8; sso_uid_tt=c58f1e24c0e9d635f00f5b1fb362a7ae; sso_uid_tt_ss=c58f1e24c0e9d635f00f5b1fb362a7ae; toutiao_sso_user=5c32092d523ddecdb2a825e60882716b; toutiao_sso_user_ss=5c32092d523ddecdb2a825e60882716b; sid_ucp_sso_v1=1.0.0-KDAzZWFmMzUxNjk1MTI4Nzg3N2ExZGQ4ODk1OTI2ZjY0NWM2MDc3YmIKHQjAgNWO4wIQzfPmqgYY7zEgDDDy4aHVBTgCQPEHGgJobCIgNWMzMjA5MmQ1MjNkZGVjZGIyYTgyNWU2MDg4MjcxNmI; ssid_ucp_sso_v1=1.0.0-KDAzZWFmMzUxNjk1MTI4Nzg3N2ExZGQ4ODk1OTI2ZjY0NWM2MDc3YmIKHQjAgNWO4wIQzfPmqgYY7zEgDDDy4aHVBTgCQPEHGgJobCIgNWMzMjA5MmQ1MjNkZGVjZGIyYTgyNWU2MDg4MjcxNmI; passport_auth_status=161f7fd86fbb82595e8a0c1b78f6a51c%2C6a8c773765bc1cefd5397baa5a1055c5; passport_auth_status_ss=161f7fd86fbb82595e8a0c1b78f6a51c%2C6a8c773765bc1cefd5397baa5a1055c5; sid_ucp_v1=1.0.0-KGNmZTVlNDZjMDI2MDViOGQxMDRiZGZhNDA3NGI3YmRmNTIzMmQxYTMKGQjAgNWO4wIQzvPmqgYY7zEgDDgCQPEHSAQaAmxxIiBhYTI4YzkwNjFhYTUwNGI2YmI3NzZhMzhjNjQwZmRkNQ; ssid_ucp_v1=1.0.0-KGNmZTVlNDZjMDI2MDViOGQxMDRiZGZhNDA3NGI3YmRmNTIzMmQxYTMKGQjAgNWO4wIQzvPmqgYY7zEgDDgCQPEHSAQaAmxxIiBhYTI4YzkwNjFhYTUwNGI2YmI3NzZhMzhjNjQwZmRkNQ; sid_guard=5c32092d523ddecdb2a825e60882716b%7C1700379086%7C5184001%7CThu%2C+18-Jan-2024+07%3A31%3A27+GMT; uid_tt=c58f1e24c0e9d635f00f5b1fb362a7ae; uid_tt_ss=c58f1e24c0e9d635f00f5b1fb362a7ae; sid_tt=5c32092d523ddecdb2a825e60882716b; sessionid=5c32092d523ddecdb2a825e60882716b; sessionid_ss=5c32092d523ddecdb2a825e60882716b; LOGIN_STATUS=1; publish_badge_show_info=%220%2C0%2C0%2C1700379097310%22; _bd_ticket_crypt_doamin=2; _bd_ticket_crypt_cookie=3d0d05b6ef426481638a8e4dfb572324; __security_server_data_status=1; store-region=cn-gd; store-region-src=uid; download_guide=%223%2F20231119%2F0%22; pwa2=%220%7C0%7C3%7C0%22; VIDEO_FILTER_MEMO_SELECT=%7B%22expireTime%22%3A1701083705243%2C%22type%22%3A1%7D; stream_player_status_params=%22%7B%5C%22is_auto_play%5C%22%3A0%2C%5C%22is_full_screen%5C%22%3A0%2C%5C%22is_full_webscreen%5C%22%3A0%2C%5C%22is_mute%5C%22%3A1%2C%5C%22is_speed%5C%22%3A1%2C%5C%22is_visible%5C%22%3A0%7D%22; dy_swidth=1920; dy_sheight=1080; strategyABtestKey=%221700802011.049%22; bd_ticket_guard_client_web_domain=2; csrf_session_id=a35196123462965bb07c7763a777f3c7; FOLLOW_NUMBER_YELLOW_POINT_INFO=%22MS4wLjABAAAA9Ax-pVKjsUPUNdV-gbVq5OBjCe9HrIGwrNnNrTUP6pQ%2F1700841600000%2F0%2F0%2F1700818725594%22; __ac_nonce=065607ee900ca2e1d9007; __ac_signature=_02B4Z6wo00f01-XWkxQAAIDChtxTfglGWJPl9peAAJwfNwYY2QEFOio3CailbYg59h6viNTvX1x-yUkoXKnPAWYhB05Cd2n-fk.FkBW2kDm7uViaS.gvPm0RVOL4P6vuYBClJ2O0WvBEqPrXfe; msToken=huLUB-XSxazA5Acrmvw9s17HL31Vn6J3BSHIUq_Erd_ijl_fNHGDNL9HKhDU6cKmS9Zgge15aY0VghcqK0ftppzEXv2U6Z15BZwpPsnEW6SQooyIezvMjzf0Ss7f; tt_scid=AF0W-D.qVNDuFq.BOSQxjUfY.SiRjmV8zOIs8JdKGR4D46DJ8SFcwEN.lcE-wbdp8ee9; odin_tt=a30b313c100e0ffa3075443f9e901dcf1344ff42a87dce72ac13714964724de0d50ac8ce2af0899c9be8babc0883b646; msToken=braWAzgTHzXaVwxbq1pdq1Y8o92nqEse6N_P-ytUz7PIzVWw5Wya_Hn-AbVKGzNmM7fGU9As3ZekQDergWAw6rACi5LdFNa0WJVhuiYdflq7W23Ile6Gkpe8OgD0; passport_fe_beating_status=false; stream_recommend_feed_params=%22%7B%5C%22cookie_enabled%5C%22%3Atrue%2C%5C%22screen_width%5C%22%3A1920%2C%5C%22screen_height%5C%22%3A1080%2C%5C%22browser_online%5C%22%3Atrue%2C%5C%22cpu_core_num%5C%22%3A16%2C%5C%22device_memory%5C%22%3A8%2C%5C%22downlink%5C%22%3A10%2C%5C%22effective_type%5C%22%3A%5C%224g%5C%22%2C%5C%22round_trip_time%5C%22%3A0%7D%22; IsDouyinActive=true; FOLLOW_LIVE_POINT_INFO=%22MS4wLjABAAAA9Ax-pVKjsUPUNdV-gbVq5OBjCe9HrIGwrNnNrTUP6pQ%2F1700841600000%2F0%2F1700823955448%2F0%22; home_can_add_dy_2_desktop=%221%22; bd_ticket_guard_client_data=eyJiZC10aWNrZXQtZ3VhcmQtdmVyc2lvbiI6MiwiYmQtdGlja2V0LWd1YXJkLWl0ZXJhdGlvbi12ZXJzaW9uIjoxLCJiZC10aWNrZXQtZ3VhcmQtcmVlLXB1YmxpYy1rZXkiOiJCQTRaOFJWNi9ORnZRSmxPT3hXMGpOeFYzQUcwcTNwcG5aSWkwZ2xoYWFTd0kwcSs4ZUloc0hwMm92eEJCdEpFT2szaGd0aDlKaVcvV3N2bHMydTg1Yzg9IiwiYmQtdGlja2V0LWd1YXJkLXdlYi12ZXJzaW9uIjoxfQ%3D%3D'
    webid = "7303072417411532314"
    msToken = "sKLFrV90_J0tjuNAYj-qAS_09943_UIcnyF4bAtDA3eRf0x0mFFxBXwvYSJL95WxDRvesQs04uA5282o7TBY3PFQvCBg0RC_AYEBzYnt9Y1rI9gCLh8zEa6YptXY"
    # result = dy.getNoteInfo(token=token, webid=webid, msToken=msToken)
    result = dy.testCookie(token=token, webid=webid, msToken=msToken)
    print(result)
    # result = dy.getUserInfo(token=token, webid=webid, msToken=msToken)
    # results = dy.getNoteList(token=token, webid=webid, msToken=msToken)
    # offset = "0"
    # num = 0
    # for i in range(0, 2):
    #     results = dy.getSearchNoteList(token=token, webid=webid, msToken=msToken, keyword="胶水", offset=offset)
    #     offset = str(int(offset) + 20)
    #     for result in results:
    #         print(result)
    #         print(num)
    #         num += 1
    #         print("-------------------")
    # for result in results:
    #     print(result)
    max_cursor = "0"

    # while True:
    #     results = dy.getNoteList(token=token, webid=webid, msToken=msToken, max_cursor=max_cursor)
    #     for result in results:
    #         print(result)
    #         max_cursor = result['max_cursor']
    #         has_more = result['has_more']
    #         print(max_cursor, has_more)
    #         if not has_more:
    #             break
    #         if max_cursor != max_cursor:
    #             time.sleep(1)
    #     # print(result)
    #     # result = dy.getNoteInfo(token=token)
