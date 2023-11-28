import hashlib
import re
import time
from datetime import datetime

import requests


class MakeRealURL(object):
    def __init__(self):
        pass

    def short_to_long(self, url):

        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36",
        }
        if len(url) < 40:
            try:
                response = requests.get(url, headers=headers)
                time.sleep(0.1)
                return response.url
            except Exception as e:
                print(e)
                return False
        else:
            return url

    def change_dyurl_user_to_modal_id(self, long_url):
        long_url = self.short_to_long(long_url)
        try:
            modal_id = re.search(r'modal_id=([^&]*)', long_url).group(1)
            url = "https://www.douyin.com/video/" + modal_id
            return url
        except:
            return False

    def makePVContentURL(self, url):
        base_xhs = "https://www.xiaohongshu.com/explore/"
        base_dy = "https://www.douyin.com/video/"
        content_id = self.makeContentID(url)
        if content_id:
            if "xiaohongshu" in url or "xhs" in url:
                return base_xhs + content_id
            elif "douyin" in url or "dy" in url:
                return base_dy + content_id
            else:
                return False
        else:
            return False

    def makeAccountURL(self, url):
        base_xhs = "https://www.xiaohongshu.com/user/profile/"
        base_dy = "https://www.douyin.com/user/"
        uid = self.makeAccountID(url)
        if uid:
            if "xiaohongshu" in url:
                return base_xhs + uid
            elif "douyin" in url:
                return base_dy + uid
            else:
                return False
        else:
            return False

    def makeAccountID(self, url):
        if "xiaohongshu" in url:
            uid = self.makeXHSAccount_id(url)
            if uid:
                return uid
            else:
                return False
        elif "douyin" in url:
            uid = self.makeDYAccount_id(url)
            if uid:
                return uid
            else:
                return False
        else:
            return False

    def makeContentID(self, url):
        url = self.short_to_long(url)
        if not url:
            return False
        if "xiaohongshu" in url:
            uid = self.makeXHSContent_id(url)
            if uid:
                return uid
            else:
                return False
        elif "douyin" in url:
            uid = self.makeDYContent_id(url)
            if uid:
                return uid
            else:
                return False
        else:
            return False

    def makeXHSAccount_id(self, url):
        url = self.short_to_long(url)
        url = url.split("?")[0] if "?" in url else url
        if "profile" in url:
            try:
                uid = re.findall(r"profile/(.+)", url)[0]
                return uid
            except:
                return False
        else:
            return False

    def makeDYAccount_id(self, url):
        # https://www.douyin.com/user/MS4wLjABAAAALXRZxTu1VpuoZpsj1AWvdM2Ik2KpepheqtWc5XjGzAc?previous_page=web_code_link
        url = self.short_to_long(url)
        url = url.split("?")[0] if "?" in url else url
        if "user" in url:
            try:
                uid = re.findall(r"user/(.+)", url)[0]
                return uid
            except:
                return False
        else:
            return False

    def makeXHSContent_id(self, url):
        url = self.short_to_long(url)
        url = url.split("?")[0] if "?" in url else url
        """https://www.xiaohongshu.com/discovery/item/64e720f1000000000b02b596"""
        if "explore" in url:
            try:
                uid = re.findall(r"explore/([^?]+)|/explore/(\w+)", url)[0]
                uid = uid[0] if uid[0] else uid[1]
                return uid
            except:
                return False
        elif "profile" in url:
            try:
                uid = re.search(r'/([^/]+)$', url).group(1)
                return uid
            except:
                return False
        elif "discovery/item" in url:
            try:
                uid = re.search(r'/item/(\w+)', url).group(1)
                return uid
            except:
                return False
        else:
            return False

    def makeDYContent_id(self, url):
        url = self.short_to_long(url)
        if "user" in url:
            try:
                uid = re.search(r'modal_id=([^&]*)', url).group(1)

                return uid
            except:
                return False
        elif "video" in url:
            uid = re.search(r'video/(\d+)/?', url).group(1)
            return uid
        else:
            return False

    def makePlatName(self, url):
        if "xiaohongshu" in url:
            return "小红书"
        elif "douyin" in url:
            return "抖音"
        else:
            return False

    def makeUniqueDayId(self, url):
        date_today = datetime.now().strftime("%Y-%m-%d")
        info = url + date_today
        return hashlib.sha1(info.encode()).hexdigest()[:20]
