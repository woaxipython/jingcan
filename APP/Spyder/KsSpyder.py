import json
import pickle
import re

import requests
from bs4 import BeautifulSoup
from requests.utils import dict_from_cookiejar, cookiejar_from_dict


class KuaiShouSpyder(object):
    def __init__(self):
        self.headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36 MicroMessenger/7.0.9.501 NetType/WIFI MiniProgramEnv/Windows WindowsWechat',
        }
        self.url = "https://www.kuaishou.com/graphql"
        self.mobile_code_url = "https://id.kuaishou.com/pass/kuaishou/sms/requestMobileCode"
        self.login_url = "https://id.kuaishou.com/pass/kuaishou/login/mobileCode"
        self.phone = "15369140121"
        self.call_back_url = "https://id.kuaishou.com/pass/kuaishou/login/passToken?callback=https%3A%2F%2Fwww.kuaishou.com%2Frest%2Finfra%2Fsts%3FfollowUrl%3Dhttps%253A%252F%252Fpassport.kuaishou.com%252Fpc%252Faccount%252FpassToken%252Fresult%253Fsuccessful%253Dtrue%2526id%253DSSO_1683530528475%2526for%253DpassTokenSuccess%26failUrl%3Dhttps%253A%252F%252Fpassport.kuaishou.com%252Fpc%252Faccount%252FpassToken%252Fresult%253Fsuccessful%253Dfalse%2526id%253DSSO_1683530528475%2526for%253DpassTokenSuccess%26setRootDomain%3Dfalse&__loginPage=https%3A%2F%2Fpassport.kuaishou.com%2Fpc%2Faccount%2FpassToken%2Fresult%3Fsuccessful%3Dfalse%26id%3DSSO_1683530528475%26for%3DpullTokenFail&sid=kuaishou.server.web"
        self.user_id = "3xeytgsat7p4x5m"
        self.note_url = "https://www.kuaishou.com/short-video/3xhcefi3qdctgew"
        self.note_base_url = "https://www.kuaishou.com/short-video/"
        with open('static/json/KuaiShouoSession.pkl', 'rb') as f:
            # with open('../../static/json/KuaiShouoSession.pkl', 'rb') as f:
            self.spyder = pickle.load(f)

    def getMobileCode(self, phone="", url=""):
        self.spyder = requests.Session()
        phone = phone if phone else self.phone
        url = url if url else self.mobile_code_url
        data = {
            "sid": "kuaishou.server.web",
            "type": "53",
            "countryCode": "+86",
            "phone": phone,
            "account": "",
            "ztIdentityVerificationType": "",
            "ztIdentityVerificationCheckToken": "",
            "channelType": "UNKNOWN",
            "encryptHeaders": "",
        }
        self.spyder.post(url, headers=self.headers, data=data)
        return {"status": "success", "message": "验证码发送成功"}

    def login(self, smsCode, phone=""):
        self.spyder = requests.Session()
        phone = phone if phone else self.phone
        data = {
            "countryCode": "+86",
            "phone": phone,
            "sid": "kuaishou.server.web",
            "createId": "true",
            "smsCode": smsCode,
            "setCookie": "true",
            "channelType": "UNKNOWN",
            "encryptHeaders": "",
        }
        self.spyder.post(self.login_url, headers=self.headers, data=data)
        # 调用callback后，才会生成完整的cookie值
        self.spyder.get(self.call_back_url, headers=self.headers)
        # with open("../../static/json/KuaiShouoSession.pkl", "wb") as f:
        with open('static/json/KuaiShouoSession.pkl', 'wb') as f:
            pickle.dump(self.spyder, f)
        return {"status": "success", "message": "登录成功"}

    def TestCookie(self, userId=""):
        user_id = userId if userId else self.user_id
        data = {
            "operationName": "visionProfile",
            "query": "query visionProfile($userId: String) {\n  visionProfile(userId: $userId) {\n    result\n    hostName\n    userProfile {\n      ownerCount {\n        fan\n        photo\n        follow\n        photo_public\n        __typename\n      }\n      profile {\n        gender\n        user_name\n        user_id\n        headurl\n        user_text\n        user_profile_bg_url\n        __typename\n      }\n      isFollowing\n      __typename\n    }\n    __typename\n  }\n}\n",
            "variables":
                {"userId": user_id}
        }
        self.headers['content-type'] = 'application/json'
        self.headers['Host'] = 'www.kuaishou.com'
        response = self.spyder.post(url=self.url, headers=self.headers, json=data)
        if response.status_code == 200 and response.json()['data']:
            print(response.json())
            if response.json()['data']['visionProfile']['result'] == 1:
                data = response.json()['data']['visionProfile']
                print(data)
                user = data['userProfile']['profile']['user_name']
                return {"status": "success", "message": "快手爬虫测试成功，成功获得{}".format(user)}
            else:
                return {"status": "failed", "message": "连接失败，请查看博主是否存在"}
        else:
            return {"status": "failed", "message": "相应失败，请登陆账号后重试"}

    def getKuaiShouUserInfo(self, url=""):
        userId = re.search('/profile/(.*)', url).group(1) if url else self.user_id
        if userId:
            data = {
                "operationName": "visionProfile",
                "query": "query visionProfile($userId: String) {\n  visionProfile(userId: $userId) {\n    result\n    hostName\n    userProfile {\n      ownerCount {\n        fan\n        photo\n        follow\n        photo_public\n        __typename\n      }\n      profile {\n        gender\n        user_name\n        user_id\n        headurl\n        user_text\n        user_profile_bg_url\n        __typename\n      }\n      isFollowing\n      __typename\n    }\n    __typename\n  }\n}\n",
                "variables":
                    {"userId": userId}
            }
            self.headers['content-type'] = 'application/json'
            self.headers['Host'] = 'www.kuaishou.com'
            response = self.spyder.post(url=self.url, headers=self.headers, json=data)
            if response.status_code == 200 and response.json()['data']:
                if response.json()['data']['visionProfile']['result'] == 1:
                    data = response.json()['data']['visionProfile']['userProfile']
                    Account_result = {
                        "nickname": data['profile']['user_name'],
                        "follow": data['ownerCount']['follow'],
                        "fans": data['ownerCount']['fan'],
                        "liked": 0,
                        "gender": "0" if data['profile']['gender'] == "F" else "1",
                        "id": data['profile']['user_id'],
                        "notes": data['ownerCount']['photo_public'],
                        "boards": "",
                        "location": "",
                        "collected": "",
                        "desc": data['profile']['user_text'],
                        "officialVerifyName": data['profile']['user_name'],
                        "red_id": "",
                        "url": url
                    }
                    return {"status": "success", "message": Account_result}
                else:
                    return {"status": "failed", "message": "连接失败，请查看博主是否存在"}
            else:
                return {"status": "failed", "message": "相应失败，请登陆账号后重试"}

    def getKuaiShouNoteInfo(self, url="", userId=""):
        url = url if url else self.note_url
        photoId = re.search('/short-video/(.*)', url).group(1)
        self.headers['Host'] = 'www.kuaishou.com'
        data = {
            "operationName": "visionProfilePhotoList",
            "query": "fragment photoContent on PhotoEntity {\n  id\n  duration\n  caption\n  originCaption\n  likeCount\n  viewCount\n  commentCount\n  realLikeCount\n  coverUrl\n  photoUrl\n  photoH265Url\n  manifest\n  manifestH265\n  videoResource\n  coverUrls {\n    url\n    __typename\n  }\n  timestamp\n  expTag\n  animatedCoverUrl\n  distance\n  videoRatio\n  liked\n  stereoType\n  profileUserTopPhoto\n  musicBlocked\n  __typename\n}\n\nfragment feedContent on Feed {\n  type\n  author {\n    id\n    name\n    headerUrl\n    following\n    headerUrls {\n      url\n      __typename\n    }\n    __typename\n  }\n  photo {\n    ...photoContent\n    __typename\n  }\n  canAddComment\n  llsid\n  status\n  currentPcursor\n  tags {\n    type\n    name\n    __typename\n  }\n  __typename\n}\n\nquery visionProfilePhotoList($pcursor: String, $userId: String, $page: String, $webPageArea: String) {\n  visionProfilePhotoList(pcursor: $pcursor, userId: $userId, page: $page, webPageArea: $webPageArea) {\n    result\n    llsid\n    webPageArea\n    feeds {\n      ...feedContent\n      __typename\n    }\n    hostName\n    pcursor\n    __typename\n  }\n}\n",
            "variables":
                {"page": "profile",
                 "pcursor": "",
                 "userId": userId}
        }
        response = self.spyder.post(url=self.url, headers=self.headers, json=data)
        if response.status_code == 200 and response.json()['data']:
            if response.json()['data']['visionProfilePhotoList']['result'] == 1:
                feeds = response.json()['data']['visionProfilePhotoList']['feeds']
                for feed in feeds:
                    if feed["photo"]["id"] == "3xcbmjy7ajs3yzy":
                        title_result = {
                            "title": feed["photo"]['caption'] if feed["photo"] else "",
                            "content_id": "",
                            "liked": feed["photo"]['caption'] if feed["photo"] else "",
                            "desc": feed["photo"]['originCaption'] if feed["photo"] else "",
                            "collected": "",
                            "forwarded": "",
                            "commented": "",
                            "imageList": [],
                            "commentList": "",
                            "hashTags": [],
                            "video_link": feed["photo"]['animatedCoverUrl'] if feed["photo"] else "",
                            "spyder_url": url,
                            "upload_time": "",
                            "content_link": url,
                            "status": "正常",
                        }
                        return {"status": "success", "message": title_result}
                    else:
                        continue
            else:
                return {"status": "failed", "message": "连接失败，请查看博主是否存在"}
        else:
            return {"status": "failed", "message": "相应失败，请登陆账号后重试"}


if __name__ == '__main__':
    ks = KuaiShouSpyder()
    # ks.getMobileCode()
    # codes = input("验证码：")
    # ks.loginKuaiShou(smsCode=codes)
    # ks.getKuaiShouNoteInfo()
    ks.getKuaiShouNoteInfo(userId="3xhbwk8wds2yrna")
