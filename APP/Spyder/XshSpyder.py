import hashlib
import json
import random
import re

import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


class GetXhsSpyder():
    def __init__(self, ):
        self.agent = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36 MicroMessenger/7.0.20.1781(0x6700143B) NetType/WIFI MiniProgramEnv/Windows WindowsWechat/WMPF XWEB/6939',
            'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36 MicroMessenger/7.0.9.501 NetType/WIFI MiniProgramEnv/Windows WindowsWechat']

        self.headers = {
            'Host': 'www.xiaohongshu.com',
            'user-agent': random.choice(self.agent),
        }

        self.base_url = 'https://www.xiaohongshu.com'
        # self.test_note_url = 'https://www.xiaohongshu.com/explore/643c87440000000013035e63?app_platform=ios&app_version=7.78&share_from_user_hidden=true&type=normal&xhsshare=WeixinSession&appuid=5c015af7000000000800d647&apptime=1678243355'
        # self.test_note_url = 'https://www.xiaohongshu.com/explore/642e5c730000000013007b5d'
        test_url = ['https://www.xiaohongshu.com/user/profile/623b189f00000000210213f8',
                    'https://www.xiaohongshu.com/explore/6468845f0000000013008a91'
                    ]
        self.test_note_url = random.choice(test_url)

        self.test_user_url = 'https://www.xiaohongshu.com/user/profile/5c015af7000000000800d647'

    def testCookie(self, token=""):
        result = self.getNoteInfo(token=token)
        if result.get("status") == "success":
            return {'status': 'success',
                    'message': "小红书测试成功，成功获取 {} 信息".format(result['message']["title"])}
        else:
            return result

    def m_md5(self, data: str):
        m = hashlib.md5()
        m.update(data.encode())
        return m.hexdigest()

    def getUserInfo(self, token, url=""):
        self.headers['authorization'] = token
        url = url if url else self.test_user_url
        if "profile" in url:
            uid = re.findall(r"profile/(.+)", url)[0]
            real_user_url = f'/fe_api/burdock/weixin/v2/user/{uid}'
            xsign = 'X' + self.m_md5(real_user_url + "WSUDD")
            self.headers['x-sign'] = xsign
            spyder_url = self.base_url + real_user_url
            response = requests.get(spyder_url, headers=self.headers, verify=False)
            if response.status_code == 200 and response.json()["success"] == True:
                data = response.json()['data']
                Account_result = {
                    "nickname": data.get("nickname", ""),
                    "follow": data.get("follows", 0),
                    "fans": data.get("fans", 0),
                    "gender": data.get("gender", 0),
                    "liked": data.get("liked", ""),
                    "account_id": data.get("id", 0),
                    "notes": data.get("notes", 0),
                    "boards": data.get("boards", 0),
                    "location": data.get("location", ""),
                    "collected": data.get("collected", 0),
                    "desc": data.get("desc", ""),
                    "officialVerifyName": data.get("officialVerifyName", ""),
                    "spyder_url": spyder_url,
                    "profile_link": url
                }
                return {'status': 'success', 'message': Account_result}
            else:
                try:
                    response_json = response.json()
                    return {'status': '1', 'message': response_json['msg']}
                except:
                    return {'status': '1', 'message': "笔记状态异常，请检查笔记是否存在"}
        else:
            return {'status': 'failed', 'message': "请输入主页连接"}

    def getNoteInfo(self, token, url=""):
        self.headers['authorization'] = token
        url = url if url else self.test_note_url
        uid = ""
        if "explore" in url:
            uid = re.findall(r"explore/([^?]+)|/explore/(\w+)", url)[0]
            uid = uid[0] if uid[0] else uid[1]
        elif "profile" in url:
            uid = re.search(r'[0-9a-zA-Z]+$', url).group() if re.search(r'[0-9a-zA-Z]+$', url) else ""
        if uid:
            real_note_url = f'/fe_api/burdock/weixin/v2/note/{uid}/single_feed'
            xsign = 'X' + self.m_md5(real_note_url + "WSUDD")
            self.headers['x-sign'] = xsign
            spyder_url = self.base_url + real_note_url
            response = requests.get(spyder_url, headers=self.headers, verify=False)

            if response.status_code == 200:
                data = response.json()['data']
                title_result = {
                    "title": data['title'],
                    "content_id": uid,
                    "liked": data['likes'],
                    "desc": data['desc'],
                    "collected": data['collects'],
                    "forwarded": data['shareCount'],
                    "commented": data['comments'],
                    "imageList": [img["url"] for img in data['imageList'] if data.get('imageList')],
                    "commentList": [data['commentList'][0]["content"] if data.get('commentList') else ""],
                    "hashTags": [tags["name"] for tags in data['hashTags'] if data.get('hashTags')],
                    "video_link": data['video']['url'] if data.get('video') else "",
                    "spyder_url": spyder_url,
                    "upload_time": data['time'],
                    "content_link": url.split("?")[0],
                }
                return {"status": "success", "message": title_result}

            else:
                try:
                    response_json = response.json()
                    return {'status': '1', 'message': response_json['msg']}
                except:
                    return {'status': '1', 'message': "笔记状态异常，请检查笔记是否存在"}
        else:
            return {'status': 'failed', 'message': "获取uid失败，请填写正确的小红书图文地址"}


if __name__ == '__main__':
    xhs = GetXhsSpyder()
    xhs.getNoteInfo()
