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


class DouYinSpyder():
    def __init__(self):
        ts = str(time.time()).split('.')[0]
        self.user_url = "https://www.douyin.com/user/MS4wLjABAAAAfjsAJZbhlKTAhClTsxbP1b04RvyTjBRPgNWzLGnMR0c"
        # self.note_url = "https://www.douyin.com/video/7218888878109904186"
        self.note_url = "https://www.douyin.com/user/MS4wLjABAAAASZj6di2175kheLW0qkCaaJSVzm3DjJqY9gpAv3DB5X3vtdA7AjAcls94-VVa3uIv?modal_id=7234598596195142970&vid=7234582445616614716"
        self.mobile_token_url = "https://sso.douyin.com/send_activation_code/v2"
        self.login_url = "https://sso.douyin.com/send_activation_code/v2"
        # self.header = {
        #     'cid': 'd9ba8ae07d955b83c3b04280f3dc5a4a',
        #     'timestamp': ts,
        #     'user-agent': 'okhttp/3.10.0.12'
        # }
        # 这里只是获取cookie，可以用playwright或selenium替代
        # res = requests.post("http://api2.52jan.com/dyapi/get_cookie/v2", data={"sign": self.set_sign()},
        #                     headers=self.header).json()
        # "cookie": res['data'][0][0]
        # print(res)
        self.headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)'
                          'Chrome/111.0.0.0 Safari/537.36', }

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
        if "user" in url:
            try:
                modal_id = re.search(r'modal_id=([^&]*)', url).group(1)
                url = "https://www.douyin.com/video/" + modal_id
            except:
                url = url
                modal_id = ""
        else:
            try:
                modal_id = re.search(r'video/([^&]*)/?', url).group(1)
            except:
                modal_id = ""
        ret = requests.get(url, headers=self.headers)

        if ret.status_code == 200:
            try:
                soup = BeautifulSoup(ret.text, 'html.parser')
                collected = re.sub(r'\D', "", soup.select('span.CE7XkkTw')[1].text)
                commented = re.sub(r'\D', "", soup.select('span.CE7XkkTw')[2].text)
                forword = re.sub(r'\D', "", soup.select('span.Uehud9DZ')[0].text)
                liked = re.sub(r'\D', "", soup.select('span.CE7XkkTw')[0].text)

                title_result = {
                    "title": soup.title.text,
                    "content_id": modal_id,
                    "liked": liked if liked else 0,
                    "desc": soup.select('p.Z_bgHH02')[0].text,
                    "collected": collected if collected else 0,
                    "commented": commented if commented else 0,
                    "forwarded": forword if forword else 0,

                    "imageList": [],
                    "commentList": [comment.text for comment in soup.select('span.VD5Aa1A1')],
                    "hashTags": [],
                    "video_link": url,
                    "spyder_url": url,
                    "upload_time": soup.select('span.aQoncqRg')[0].text.replace("发布时间：", ""),
                    "content_link": url,
                }
                return {"status": "success", "message": title_result}
            except:
                return {"status": "1", "message": "异常"}
        else:
            return {"status": "failed", "message": "获取抖音数据出错"}

    def testCookie(self, token):
        result = self.getUserInfo(token=token)
        if result.get("status") == "success":
            return {'status': 'success',
                    'message': "抖音测试成功，成功获取 {} 信息".format(result['message']["nickname"])}
        else:
            return result

    def getUserInfo(self, token, url=""):
        self.headers['cookie'] = token
        url = url if url else self.user_url
        ret = requests.get(url, headers=self.headers)
        if ret.status_code == 200:
            soup = BeautifulSoup(ret.text, 'html.parser')
            Account_result = {
                "nickname": soup.select('div.HqxPzh_q')[0].text if soup.select('div.HqxPzh_q') else "",
                "follow": int(self.changeNumber(soup.select('div.TxoC9G6_')[0].text)) if soup.select(
                    'div.TxoC9G6_') else 0,
                "fans": int(self.changeNumber(soup.select('div.TxoC9G6_')[1].text)) if soup.select(
                    'div.TxoC9G6_') else 0,
                "gender": None,
                "liked": int(self.changeNumber(soup.select('div.TxoC9G6_')[2].text)) if soup.select(
                    'div.TxoC9G6_') else 0,
                "account_id": soup.select('span.aH7rLkZZ')[0].text if soup.select('span.aH7rLkZZ') else "",
                "notes": int(soup.select('span.J6IbfgzH')[0].text) if soup.select('span.J6IbfgzH') else 0,
                "boards": None,
                "location": soup.select('span.a83NyFJ4')[0].text if soup.select('span.a83NyFJ4') else "",
                "collected": None,
                "desc": soup.select('span.Nu66P_ba')[1].text if soup.select('span.Nu66P_ba') else "",
                "officialVerifyName": soup.select('div.HqxPzh_q')[0].text if soup.select('div.HqxPzh_q') else "",
                "profile_link": url,
                "spyder_url": url,
            }
            if Account_result["nickname"] != "":
                return {'status': 'success', 'message': Account_result}
            else:
                return {"status": "failed", "message": "获取抖音数据出错"}
        else:
            return {"status": "failed", "message": "获取抖音数据出错"}

    def changeNumber(self, number_str):
        if "万" in number_str:
            number_str = number_str.replace("万", "")
        return str(int(float(number_str) * 10000))


if __name__ == '__main__':
    # url = "https://www.douyin.com/video/7214409188234120487"
    # url = "https://www.douyin.com/user/MS4wLjABAAAAj_5sNno0lusPp1AOp6h0tvPxELuPxI1Q5DyxmEJ7x_4?modal_id=7218888878109904186"
    dy = DouYinSpyder()
    token = 'ttwid=1%7CNvLn_dFZxi5e7vG7FHjiNooA_0VOzam6PJZ77OPdfiM%7C1681889128%7C2cc1a98c7532fc3194aeffe9238bc6a422a3dba39a6d5d4abf8116d851a26158; passport_csrf_token=b8e30d7d38b232c46b41fefe0c471d17; passport_csrf_token_default=b8e30d7d38b232c46b41fefe0c471d17; s_v_web_id=verify_lgndd2ax_s5kCld9F_I7TG_4LTK_8y1V_CMpjQQjgH1qC; pwa2=%223%7C0%22; ttcid=1cbda62ceff94064bb877f7e6c52732f39; strategyABtestKey=%221684403170.925%22; __ac_nonce=064660a41005452bdf4bc; __ac_signature=_02B4Z6wo00f01h0e6fQAAIDCnRwTtwxbJO4dPu1AAOMvxPzbso-FvWV08uLJocXrMEVTA8W5.Ec3KZQouFyA3X1GuiPhkxTpd.AmY93e4QZGYVcsF98Hvl6IDHk8CVaw8D17Y87l8h9Sik.2af; download_guide=%223%2F20230518%22; douyin.com; d_ticket=ec7e699b5c2118fcd3faaa84e70b895b72c94; passport_assist_user=Cjz1O9l9Az1Q55mknWxfoYEGxOvHZqZev1FgFZo_usknPvGPOG1sLLVGaAbMwJzdwcvOsXsAEvmUWzCxOggaSAo8PUytSvd7xKs6k0od6pjbnw1D5wd29-rQH_BDqoh8y4K-GP9yujAB2-ClQgdEzwARmcRmypj1fHlPQe-TEK27sQ0Yia_WVCIBA6nd_N0%3D; n_mh=acm93QdnGeokQ8P9OssEFwOxgViwjjf-3wI379AUXj0; sso_auth_status=1e8efa73012bd7f252e39d07c634a9cc; sso_auth_status_ss=1e8efa73012bd7f252e39d07c634a9cc; sso_uid_tt=e46edc4ec726a056f711db0e1a8bb60c; sso_uid_tt_ss=e46edc4ec726a056f711db0e1a8bb60c; toutiao_sso_user=263c5d87974c6ba4fa2f2dc6482ea097; toutiao_sso_user_ss=263c5d87974c6ba4fa2f2dc6482ea097; sid_ucp_sso_v1=1.0.0-KDBhNWY2MTAxOWRjMzA0NDYyMjdjYjgwOTlkNGUzYjNkNDcxNGUwYWMKHQjAgNWO4wIQl5eYowYY7zEgDDDy4aHVBTgCQPEHGgJobCIgMjYzYzVkODc5NzRjNmJhNGZhMmYyZGM2NDgyZWEwOTc; ssid_ucp_sso_v1=1.0.0-KDBhNWY2MTAxOWRjMzA0NDYyMjdjYjgwOTlkNGUzYjNkNDcxNGUwYWMKHQjAgNWO4wIQl5eYowYY7zEgDDDy4aHVBTgCQPEHGgJobCIgMjYzYzVkODc5NzRjNmJhNGZhMmYyZGM2NDgyZWEwOTc; odin_tt=ac36a113358aa14bb2aa885d2dc483a3c7918f55e4ed76cf4ad982fcb128c943fee90a255e6f434be3ec5e586083a711; passport_auth_status=f79ac2e6db0d7c4e7caca42ee1061f04%2Cb81ba07f3de81cc75f02101940062756; passport_auth_status_ss=f79ac2e6db0d7c4e7caca42ee1061f04%2Cb81ba07f3de81cc75f02101940062756; uid_tt=9bc02b6263804a3f5495c4c9205a625c; uid_tt_ss=9bc02b6263804a3f5495c4c9205a625c; sid_tt=d1aad2c5dd6505edf1820b01e608a1e9; sessionid=d1aad2c5dd6505edf1820b01e608a1e9; sessionid_ss=d1aad2c5dd6505edf1820b01e608a1e9; publish_badge_show_info=%220%2C0%2C0%2C1684409242734%22; VIDEO_FILTER_MEMO_SELECT=%7B%22expireTime%22%3A1685014042761%2C%22type%22%3A1%7D; FOLLOW_LIVE_POINT_INFO=%22MS4wLjABAAAA9Ax-pVKjsUPUNdV-gbVq5OBjCe9HrIGwrNnNrTUP6pQ%2F1684425600000%2F0%2F1684409243125%2F0%22; LOGIN_STATUS=1; store-region=cn-gd; store-region-src=uid; home_can_add_dy_2_desktop=%221%22; sid_guard=d1aad2c5dd6505edf1820b01e608a1e9%7C1684409243%7C5183999%7CMon%2C+17-Jul-2023+11%3A27%3A22+GMT; sid_ucp_v1=1.0.0-KGFiZDU1OGJjN2RlNWExMjAwZjUwMDVkNTVjNDU4YzUzMDYzOTQ3OTYKGQjAgNWO4wIQm5eYowYY7zEgDDgCQPEHSAQaAmxmIiBkMWFhZDJjNWRkNjUwNWVkZjE4MjBiMDFlNjA4YTFlOQ; ssid_ucp_v1=1.0.0-KGFiZDU1OGJjN2RlNWExMjAwZjUwMDVkNTVjNDU4YzUzMDYzOTQ3OTYKGQjAgNWO4wIQm5eYowYY7zEgDDgCQPEHSAQaAmxmIiBkMWFhZDJjNWRkNjUwNWVkZjE4MjBiMDFlNjA4YTFlOQ; csrf_session_id=532b1cf3fc3c148eaff7458b61c79baa; bd_ticket_guard_server_data=; bd_ticket_guard_client_data=eyJiZC10aWNrZXQtZ3VhcmQtdmVyc2lvbiI6MiwiYmQtdGlja2V0LWd1YXJkLWl0ZXJhdGlvbi12ZXJzaW9uIjoxLCJiZC10aWNrZXQtZ3VhcmQtY2xpZW50LWNlcnQiOiItLS0tLUJFR0lOIENFUlRJRklDQVRFLS0tLS1cbk1JSUNFekNDQWJxZ0F3SUJBZ0lVUE5UKzhjSzdER3RldHcya0YyQTVSNGx6SkFBd0NnWUlLb1pJemowRUF3SXdcbk1URUxNQWtHQTFVRUJoTUNRMDR4SWpBZ0JnTlZCQU1NR1hScFkydGxkRjluZFdGeVpGOWpZVjlsWTJSellWOHlcbk5UWXdIaGNOTWpNd05URTRNVEV5TnpJd1doY05Nek13TlRFNE1Ua3lOekl3V2pBbk1Rc3dDUVlEVlFRR0V3SkRcblRqRVlNQllHQTFVRUF3d1BZbVJmZEdsamEyVjBYMmQxWVhKa01Ga3dFd1lIS29aSXpqMENBUVlJS29aSXpqMERcbkFRY0RRZ0FFeCtDVDNETy9BWkdNTXAwS1hBYjlqcThwTUE5T2RGQUExODFqZUZqK2wwa1d4S0ZQUDBURm9GRndcbno3L1RhbEZKVXNDSnBEdjJuTGQ5clBjY0FiY28zYU9CdVRDQnRqQU9CZ05WSFE4QkFmOEVCQU1DQmFBd01RWURcblZSMGxCQ293S0FZSUt3WUJCUVVIQXdFR0NDc0dBUVVGQndNQ0JnZ3JCZ0VGQlFjREF3WUlLd1lCQlFVSEF3UXdcbktRWURWUjBPQkNJRUlOcWVRSDI2NFMvRlBJazlVRHdvVjhRa3FVL0JXTkh6M2gwRkl4bGlBSFQzTUNzR0ExVWRcbkl3UWtNQ0tBSURLbForcU9aRWdTamN4T1RVQjdjeFNiUjIxVGVxVFJnTmQ1bEpkN0lrZURNQmtHQTFVZEVRUVNcbk1CQ0NEbmQzZHk1a2IzVjVhVzR1WTI5dE1Bb0dDQ3FHU000OUJBTUNBMGNBTUVRQ0lFZ1pJNUJzSFZlcXJBWDZcbmFvaUJSQXhSN29kVDhmTTJ0RTdMNGNVeXFkQmJBaUJlTk1pZzUwdVJEMjFoVzhHRTcvOXdHR3I2Q0hJK1BSVUFcbjlGSFlMZzA3a2c9PVxuLS0tLS1FTkQgQ0VSVElGSUNBVEUtLS0tLVxuIn0=; msToken=q3swEkrVbYpGLEHOXttLCSSBkXQa7NPtkF1WGPPGRZKuQBAB1P0EfgDD7frClweAUHjeE9_GwhTVIkuRmtmfrW5trqcFyhmaWru5YOc2ekHFuAWCsRwYeA==; tt_scid=U3kcLqUtZWMVGP-Te9v9s2dyY3wqSZNh91egu.vQtyxQmH.fkZmSGGx5TIcdeXcFe414; msToken=SBKqYut1erJlvFpq5dS0Obkcu04XEeDfar19o131FDSOJTZBQdbO-xK8b9bneWijk9PKH9VOiiMozv5YySpBH0ywCiP0tAxS4rNB0HVbwwG0MWoZNkqpMw==; passport_fe_beating_status=false'
    result = dy.getNoteInfo(token=token)
    print(result)
