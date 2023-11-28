import time
import urllib.parse
import datetime

import execjs

# js = execjs.compile(open(r'makeDYInfo/dy.js', 'r', encoding='gb18030').read())
js = execjs.compile(open(r'APP/Spyder/makeDYInfo/dy.js', 'r', encoding='gb18030').read())


def testNotice(response):
    try:
        notice = response.json()['filter_detail']['notice']
        if notice:
            return notice
        else:
            return True
    except:
        return True


def makeNotesSpyderURL(webid, msToken, sec_user_id, max_cursor):
    list_url = "https://www.douyin.com/aweme/v1/web/aweme/post/"
    params = get_user_note_params(webid, msToken, sec_user_id, max_cursor)
    splice_url_str = splice_url(params)
    xs = js.call('get_dy_xb', splice_url_str)
    params['X-Bogus'] = xs
    spyder_url = list_url + '?' + splice_url(params)
    return spyder_url


def makeProfileSpyderURL(webid, msToken, sec_user_id):
    spyder_url = "https://www.douyin.com/aweme/v1/web/user/profile/other/?"
    params = get_profile_params(webid, msToken, sec_user_id)
    splice_url_str = splice_url(params)
    xs = js.call('get_dy_xb', splice_url_str)
    params['X-Bogus'] = xs
    spyder_url = spyder_url + splice_url(params)
    return spyder_url


def makeSearchNoteSpyderURL(webid, msToken, keyword, sort_type, offset):
    search_url = "https://www.douyin.com/aweme/v1/web/general/search/single/?"
    params = get_search_note_params(webid, msToken, keyword, sort_type, offset)
    splice_url_str = splice_url(params)
    xs = js.call('get_dy_xb', splice_url_str)
    params['X-Bogus'] = xs
    spyder_url = search_url + splice_url(params)
    print(spyder_url)
    return spyder_url


def splice_url(params):
    splice_url_str = ''
    for key, value in params.items():
        if value is None:
            value = ''
        splice_url_str += key + '=' + value + '&'
    return splice_url_str[:-1]


def get_headers():
    return {
        "authority": "www.douyin.com",
        "accept": "application/json, text/plain, */*",
        "accept-language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
        "cache-control": "no-cache",
        "pragma": "no-cache",
        "referer": "https://www.douyin.com/user/MS4wLjABAAAAigSKToDtKeC5cuZ3YsDrHfYuvpLqVSygIZ0m0yXfUAI",
        "sec-ch-ua": "\"Microsoft Edge\";v=\"117\", \"Not;A=Brand\";v=\"8\", \"Chromium\";v=\"117\"",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "\"Windows\"",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36 Edg/117.0.2045.47"
    }


def get_note_params(webid, msToken, modal_id):
    return {
        "device_platform": "webapp",
        "aid": "6383",
        "channel": "channel_pc_web",
        "aweme_id": modal_id,
        "pc_client_type": "1",
        "version_code": "190500",
        "version_name": "19.5.0",
        "cookie_enabled": "TRUE",
        "screen_width": "1920",
        "screen_height": "1080",
        "browser_language": "zh-CN",
        "browser_platform": "Win32",
        "browser_name": "Chrome",
        "browser_version": "114.0.0.0",
        "browser_online": "TRUE",
        "engine_name": "Blink",
        "engine_version": "114.0.0.0",
        "os_name": "Windows",
        "os_version": "10",
        "cpu_core_num": "16",
        "device_memory": "8",
        "platform": "PC",
        "downlink": "7.7",
        "effective_type": "4g",
        "round_trip_time": "100",
        "webid": webid,
        "msToken": msToken,
    }


def get_profile_params(webid, msToken, sec_user_id):
    return {
        "device_platform": "webapp",
        "aid": "6383",
        "channel": "channel_pc_web",
        "publish_video_strategy_type": "2",
        "source": "channel_pc_web",
        "sec_user_id": sec_user_id,
        "pc_client_type": "1",
        "version_code": "170400",
        "version_name": "17.4.0",
        "cookie_enabled": "true",
        "screen_width": "1707",
        "screen_height": "1067",
        "browser_language": "zh-CN",
        "browser_platform": "Win32",
        "browser_name": "Edge",
        "browser_version": "117.0.2045.47",
        "browser_online": "true",
        "engine_name": "Blink",
        "engine_version": "117.0.0.0",
        "os_name": "Windows",
        "os_version": "10",
        "cpu_core_num": "20",
        "device_memory": "8",
        "platform": "PC",
        "downlink": "10",
        "effective_type": "4g",
        "round_trip_time": "50",
        "webid": webid,
        # "webid": "7303072417411532314",
        # "msToken": "rCasLwylPrkYXfqOpkyoV47dPbeOH9ezXdKrnkuR5rWZSe1ld4kjkZHD8xbobObGm-hraDQvOSJLZtEMwM_hr4NnGGQbqGg1jsBOin0-xQ6Ku4-9MgfagAHmZK8=",
        "msToken": msToken,

    }


def get_user_note_params(webid, msToken, sec_user_id, max_cursor):
    return {
        "device_platform": "webapp",
        "aid": "6383",
        "channel": "channel_pc_web",
        "sec_user_id": sec_user_id,
        "max_cursor": max_cursor,
        "locate_query": "false",
        "show_live_replay_strategy": "1",
        "need_time_list": "1",
        "time_list_query": "0",
        "whale_cut_token": "",
        "cut_version": "1",
        "count": "18",
        "publish_video_strategy_type": "2",
        "pc_client_type": "1",
        "version_code": "170400",
        "version_name": "17.4.0",
        "cookie_enabled": "true",
        "screen_width": "1707",
        "screen_height": "1067",
        "browser_language": "zh-CN",
        "browser_platform": "Win32",
        "browser_name": "Edge",
        "browser_version": "117.0.2045.47",
        "browser_online": "true",
        "engine_name": "Blink",
        "engine_version": "117.0.0.0",
        "os_name": "Windows",
        "os_version": "10",
        "cpu_core_num": "20",
        "device_memory": "8",
        "platform": "PC",
        "downlink": "10",
        "effective_type": "4g",
        "round_trip_time": "50",
        # "webid": "7285297037532612107",
        "webid": webid,
        "msToken": msToken,
        # "msToken": "rCasLwylPrkYXfqOpkyoV47dPbeOH9ezXdKrnkuR5rWZSe1ld4kjkZHD8xbobObGm-hraDQvOSJLZtEMwM_hr4NnGGQbqGg1jsBOin0-xQ6Ku4-9MgfagAHmZK8=",
    }


def get_search_note_params(webid, msToken, keyword, sort_type, offset=0):
    return {
        "device_platform": "webapp",
        "count": "25",
        "sort_type": sort_type,
        "keyword": keyword,
        "aid": "6383",
        "offset": offset,
        "channel": "channel_pc_web",
        "publish_video_strategy_type": "2",
        "source": "channel_pc_web",
        "sec_user_id": "",
        "pc_client_type": "1",
        "version_code": "170400",
        "version_name": "17.4.0",
        "cookie_enabled": "true",
        "screen_width": "1707",
        "screen_height": "1067",
        "browser_language": "zh-CN",
        "browser_platform": "Win32",
        "browser_name": "Edge",
        "browser_version": "117.0.2045.47",
        "browser_online": "true",
        "engine_name": "Blink",
        "engine_version": "117.0.0.0",
        "os_name": "Windows",
        "os_version": "10",
        "cpu_core_num": "20",
        "device_memory": "8",
        "platform": "PC",
        "downlink": "10",
        "effective_type": "4g",
        "round_trip_time": "50",
        # "webid": "7285671865124996668",
        "webid": webid,
        "msToken": msToken, }


def get_note_info(data, url, modal_id):
    upload_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(data.get("create_time")))
    account_id = data.get("author").get('sec_uid')
    return {
        "title": data.get("desc"),
        "content_id": modal_id,
        "liked": data.get("statistics").get("digg_count"),
        "desc": data.get("statistics").get("desc"),
        "collected": data.get("statistics").get("collect_count"),
        "commented": data.get("statistics").get("comment_count"),
        "forwarded": data.get("statistics").get("share_count"),
        "imageList": "[]",
        "commentList": "[]",
        "hashTags": "[]",
        "video_link": url,
        "spyder_url": url,
        "upload_time": upload_time,
        "contenttype": "视频",
        "upgrade_time": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "content_link": url,
        "status": "正常",
        "account_plat_id": account_id,
        "profile_link": "https://www.douyin.com/user/" + account_id,

    }


def get_profile_info(data, url, modal_id):
    return {
        "nickname": data.get("nickname", ""),
        "follow": data.get("following_count", ""),
        "fans": data.get("follower_count", ""),
        "gender": data.get("gender", 0),
        "liked": data.get("total_favorited", ""),
        "account_id": modal_id,
        "notes": data.get("aweme_count", 0),
        "boards": "",
        "location": data.get("ip_location", ""),
        "collected": data.get("collected", 0),
        "desc": data.get("signature", ""),
        "upgradetime": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "officialVerifyName": data.get("officialVerifyName", ""),
        "spyder_url": url,
        "profile_link": url,
        "status": "正常",
    }


def get_user_note_info(note):
    return {
        "title": note['desc'],
        "content_id": note['aweme_id'],
        "liked": note['statistics']['digg_count'],
        "desc": note['desc'],
        "collected": note['statistics']['collect_count'],
        "forwarded": note['statistics']['share_count'],
        "commented": note['statistics']['comment_count'],
        "imageList": "",
        "commentList": "",
        "hashTags": "",
        "upgrade_time": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "video_link": "https://www.douyin.com/video/" + note['aweme_id'],
        "contenttype": "视频",
        "spyder_url": "",
        "upload_time": datetime.datetime.fromtimestamp(note['create_time']).strftime("%Y-%m-%d %H:%M:%S"),
        "content_link": "https://www.douyin.com/video/" + note['aweme_id'],
        "status": "正常",
    }


def get_search_note_info(data):
    return {
        "title": data['desc'],
        "content_id": data['aweme_id'],
        "liked": data['statistics']['digg_count'],
        "desc": data['desc'],
        "collected": data['statistics']['collect_count'],
        "forwarded": data['statistics']['share_count'],
        "commented": data['statistics']['comment_count'],
        "imageList": str(data['images']),
        "commentList": "",
        "hashTags": "",
        "upgrade_time": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "video_link": "https://www.douyin.com/video/" + data['aweme_id'],
        "contenttype": "视频",
        "spyder_url": "",
        "upload_time": datetime.datetime.fromtimestamp(data['create_time']).strftime("%Y-%m-%d %H:%M:%S"),
        "content_link": "https://www.douyin.com/video/" + data['aweme_id'],
        "status": "正常",
    }
