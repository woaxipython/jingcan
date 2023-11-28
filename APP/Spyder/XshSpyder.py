import hashlib
import json
import random
import re

import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning

from APP.Spyder.makeRealURL import MakeRealURL
from APP.Spyder.makeXHSInfo.makeInfo import get_note_info, getHeaders, makeUserSpyderURL, get_profile_info, \
    get_user_note, makeNotesSpyderURL, makeNoteSpyderURL

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

makeRealURL = MakeRealURL()


class GetXhsSpyder():
    def __init__(self, ):
        self.headers = getHeaders()

        self.base_url = 'https://www.xiaohongshu.com'
        test_url = ['https://www.xiaohongshu.com/user/profile/623b189f00000000210213f8',
                    'https://www.xiaohongshu.com/explore/6468845f0000000013008a91'
                    ]
        self.test_note_url = random.choice(test_url)
        self.test_user_url = 'https://www.xiaohongshu.com/user/profile/63454e9000000000180216d9'

    def testCookie(self, token=""):
        result = self.getNoteInfo(token=token)
        if result.get("status") == "1":
            return {'status': '1',
                    'message': "小红书测试成功，成功获取 {} 信息".format(result['message']["title"])}
        else:
            return result

    def getUserInfo(self, token, url=""):
        self.headers['authorization'] = token
        url = url if url else self.test_user_url
        uid = makeRealURL.makeXHSAccount_id(url)
        if not uid:
            return {'status': '0', 'message': "请输入正确的主页连接"}
        spyder_url, headers = makeUserSpyderURL(uid, self.headers)
        response = requests.get(spyder_url, headers=headers, verify=False)
        if not response.status_code == 200 and not response.json()["success"] == True:
            try:
                response_json = response.json()
                return {'status': '2', 'message': response_json['msg']}
            except:
                return {'status': '3', 'message': "账号异常，请检查账号是否存在"}
        result = get_profile_info(response, url, spyder_url)
        return {'status': '1', 'message': result}

    def getNoteList(self, token, page, url=""):
        self.headers['authorization'] = token
        url = url if url else self.test_user_url
        if not "profile" in url:
            yield {'status': '0', 'message': "请输入正确的主页连接"}
        spyder_url, headers = makeNotesSpyderURL(url, page, self.headers)
        response = requests.get(spyder_url, headers=headers, verify=False)
        if not response.status_code == 200 and not response.json()["success"] == True:
            try:
                response_json = response.json()
                yield {'status': '2', 'message': response_json['msg']}
            except:
                yield {'status': '2', 'message': "笔记状态异常，请检查笔记是否存在"}
        for note in response.json()['data']:
            result = get_user_note(note)
            yield {'status': '1', 'message': result}

    def getNoteInfo(self, token, url=""):
        self.headers['authorization'] = token
        url = url if url else self.test_note_url
        uid = makeRealURL.makeXHSContent_id(url)
        if not uid:
            return {'status': '0', 'message': "请输入正确的笔记连接"}
        spyder_url, headers = makeNoteSpyderURL(uid, self.headers)
        response = requests.get(spyder_url, headers=headers, verify=False)
        if not response.status_code == 200:
            try:
                response_json = response.json()
                return {'status': '2', 'message': response_json['msg']}
            except:
                return {'status': '3', 'message': "笔记不存在"}

        result = get_note_info(response, spyder_url, url, uid)
        return {"status": "1", "message": result}


if __name__ == '__main__':
    xhs = GetXhsSpyder()
    download_url = "http://v.xiaohongshu.com/stream/110/259/01e468842fba380e010370038838517ae1_259.mp4?sign=4f48cb6a71f147292f6ee8afe2e76f25&t=655ee1d3"
    token = "wxmp.25d57530-68bd-47a1-9d77-3ac796bda046"
    # filename = "test.mp4"
    # for page in range(1, 3):
    #     ass = xhs.getNoteList(token=token, page=page)
    #     for a in ass:
    #         print(a)
    result = xhs.getUserInfo(token=token)
    print(result)