import datetime
import hashlib
import re
import time
import random
from urllib import parse

base_url = 'https://www.xiaohongshu.com'


def m_md5(data: str):
    m = hashlib.md5()
    m.update(data.encode())
    return m.hexdigest()


def makeNoteSpyderURL(uid, headers):
    real_note_url = f'/fe_api/burdock/weixin/v2/note/{uid}/single_feed'
    xsign = 'X' + m_md5(real_note_url + "WSUDD")
    headers['x-sign'] = xsign
    spyder_url = base_url + real_note_url
    return spyder_url, headers


def makeUserSpyderURL(uid, headers):
    real_user_url = f'/fe_api/burdock/weixin/v2/user/{uid}'
    xsign = 'X' + m_md5(real_user_url + "WSUDD")
    headers['x-sign'] = xsign
    spyder_url = base_url + real_user_url
    return spyder_url, headers


def makeNotesSpyderURL(url, page, headers):
    uid = re.findall(r"profile/(.+)", url)[0]
    real_user_url = f'/fe_api/burdock/weixin/v2/user/{uid}/notes?page={page}'
    xsign = 'X' + m_md5(real_user_url + "WSUDD")
    headers['x-sign'] = xsign
    spyder_url = base_url + real_user_url
    return spyder_url, headers


def makeSearchNotesSpyderURL(headers, keyword, page, sort_by):
    # real_user_url = f'fe_api/burdock/weixin/v2/search/notes?keyword={keyword}&sortBy=hot_desc&page={page}&pageSize=20&needGifCover=true&sid=session.1575338664880906512653'
    # "fe_api/burdock/weixin/v2/search/notes?keyword=%E6%9D%AD%E5%B7%9E%E4%BA%B2%E5%AD%90&sortBy=hot_desc&page={}&pageSize=20&needGifCover=true&sid=session.1575338664880906512653"
    real_user_url = '/fe_api/burdock/weixin/v2/search/notes?keyword={}&sortBy={}' \
                    '&page={}&pageSize=20&prependNoteIds=&needGifCover=true'.format(parse.quote(keyword),
                                                                                    sort_by,
                                                                                    page + 1)
    xsign = 'X' + m_md5(real_user_url + "WSUDD")
    headers['x-sign'] = xsign
    spyder_url = base_url + real_user_url
    return spyder_url, headers


def getHeaders():
    agent = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36 MicroMessenger/7.0.20.1781(0x6700143B) NetType/WIFI MiniProgramEnv/Windows WindowsWechat/WMPF XWEB/6939',
        'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36 MicroMessenger/7.0.9.501 NetType/WIFI MiniProgramEnv/Windows WindowsWechat']

    return {
        'Host': 'www.xiaohongshu.com',
        'user-agent': random.choice(agent),
    }


def get_note_info(response, spyder_url, url, uid):
    data = response.json()['data']
    account_id = data['user']['id']
    return {
        "title": data['title'],
        "content_id": uid,
        "liked": data['likes'],
        "desc": data['desc'],
        "collected": data['collects'],
        "forwarded": data['shareCount'],
        "commented": data['comments'],
        "imageList": str([img["url"] for img in data['imageList'] if data.get('imageList')]),
        "commentList": [data['commentList'][0]["content"] if data.get('commentList') else ""],
        "hashTags": str([tags["name"] for tags in data['hashTags'] if data.get('hashTags')]),
        "video_link": data['video']['url'] if data.get('video') else "",
        "spyder_url": spyder_url,
        "upload_time": data['time'],
        "content_link": url.split("?")[0],
        "contenttype": "图文",
        "upgrade_time": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "status": "正常",
        "account_plat_id": data['user']['id'],
        "profile_link": "https://www.xiaohongshu.com/user/profile/" + account_id,
    }


def get_profile_info(response, url, spyder_url):
    data = response.json()['data']
    return {
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
        "upgradetime": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "officialVerifyName": data.get("officialVerifyName", ""),
        "spyder_url": spyder_url,
        "profile_link": url,
        "status": "正常",
    }


def get_user_note(note):
    return {
        "title": note['title'],
        "content_id": note['id'],
        "liked": note['likes'],
        "desc": "",
        "collected": note['collects'],
        "forwarded": "",
        "commented": note['comments'],
        "imageList": "",
        "commentList": "",
        "hashTags": "",
        "video_link": "",
        "spyder_url": "",
        "contenttype": "图文",
        "upgrade_time": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "upload_time": note['time'],
        "content_link": "https://www.xiaohongshu.com/explore/" + note['id'],
        "status": "正常",
    }


def get_search_note_info(note):
    return {"title": note['title'],
            "content_id": note['id'],
            "liked": note['likes'],
            "desc": "",
            "collected": note['collects'],
            "forwarded": "",
            "commented": note['comments'],
            "imageList": "",
            "commentList": "",
            "hashTags": "",
            "upgrade_time": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "video_link": "",
            "contenttype": "图文",
            "spyder_url": "",
            "upload_time": note['time'],
            "content_link": "https://www.xiaohongshu.com/explore/" + note['id'],
            "status": "正常", }
