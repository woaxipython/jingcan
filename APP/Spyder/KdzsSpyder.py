import base64
import json
import os
import time

import requests
import pickle

import jwt


class KuaiDiZhuShouSpyder():
    def __init__(self):
        # with open("static/json/data.json") as f:
        with open("static/json/data.json") as f:
            # with open("../../static/json/data.json") as f:
            self.token = json.load(f)["Token"]
        with open('static/json/session.pkl', 'rb') as f:
            # with open('../../static/json/session.pkl', 'rb') as f:
            self.spyder = pickle.load(f)
        self.captcha_url = "https://erp.kuaidizs.cn/index/user/getCaptcha"
        self.login_url = "https://erp.kuaidizs.cn/index/user/login"
        self.search_url = "https://erp.kuaidizs.cn/trade/queryTrade"
        self.addBrand_url = "https://erp.kuaidizs.cn/item/brand/save"
        self.addSaleProduct_url = "https://erp.kuaidizs.cn/item/sysItem/save"
        self.store_url = "https://erp.kuaidizs.cn/index/platformShop/getPlatformShops"
        self.test_url = "https://erp.kuaidizs.cn/index.html?userId=21db3051cbf2301533db43df6fb620a2#/"
        self.refund_url = "https://erp.kuaidizs.cn/aftersale/selectRefundListWithPage"
        self.hand_order_url = "https://erp.kuaidizs.cn/trade/handTrade/importExcel"
        self.progress_url = "https://erp.kuaidizs.cn/item/async/getProgress"
        self.create_url = 'https://erp.kuaidizs.cn/trade/handTrade/created'
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36"
        }
        self.headers["qnquerystring"] = self.token

    def getCaptcha(self):
        # 获取验证码
        response = self.spyder.get(self.captcha_url, headers=self.headers).json()["data"]  # image/png;base64 数据
        decoded = base64.b64decode(response)
        with open('static/images/captcha.png', 'wb') as f:
            f.write(decoded)
        return {"status": "success", "message": "已更新"}

    def login(self, account, password, captcha, vscode=""):
        login_data = {
            "accountName": account,
            "captcha": captcha,
            "loginType": 1,
            "password": password,
            "verifyCode": vscode
        }
        response = self.spyder.post(self.login_url, json=login_data, headers=self.headers)
        print(response.json())
        if response.json()["success"]:
            self.token = response.headers["qnquerystring"]

            save_json = {}
            save_json["Token"] = self.token
            # 触发手机验证码标头
            # "{"data":null,"errorCode":1063,"errorMessage":"当前登录需要二次验证，短信验证码已发送至（********0121）","success":false}"
            with open("static/json/session.pkl", "wb") as f:
                pickle.dump(self.spyder, f)
            with open("static/json/data.json", "w") as f:
                json.dump(save_json, f)
            return {"status": "success", "message": json.dumps(response.json())}
        else:
            return {"status": "failed", "message": response.json()["errorMessage"]}

    def TestCookie(self):

        decoded = jwt.decode(self.token, options={'verify_signature': False}, algorithms=['HS256'])
        timestamp = decoded["exp"]
        if timestamp > time.time():
            response = self.spyder.get(self.test_url, headers=self.headers)
            print(response.text)
            if response.status_code == 200:
                return {"status": "success", "message": "验证通过，可正常登录"}
            else:
                return {"status": "failed", "message": "令牌未过期，但不可登录"}
        else:
            return {"status": "failed", "message": "令牌已过期"}

    def createTrade(self, form_dict, order_list, shipInfo, search_id):
        json = {"createTime": "",
                "discount": "0.00",
                "num": len(order_list),
                "orderNum": len(order_list),
                "orders": order_list,
                "payment": "",
                "platform": "other",
                "postFee": 0,
                "receiverAddress": form_dict.get("handOrderAddress"),
                "receiverCity": "",
                "receiverCounty": "",
                "receiverMobile": "",
                "receiverName": form_dict.get("handOrderName"),
                "receiverPhone": form_dict.get("handOrderPhone"),
                "receiverProvince": "",
                "remarkFlag": "",
                "sellerId": "168188696251881",
                "sellerMemo": "",
                "sellerNick": "分销",
                "senderAddress": "",
                "senderCity": "",
                "senderCounty": "",
                "senderMobile": "",
                "senderName": "",
                "senderPhone": "",
                "senderProvince": "",
                "shipInfo": shipInfo,
                "tid": search_id,
                "weight": 0, }
        response = self.spyder.post(self.create_url, json=json, headers=self.headers)
        if not response.json()['success']:
            return {"status": False, "message": response.json()["errorMessage"]}
        else:
            return {"status": True, "message": "上传订单成功"}

    def getOrder(self, stores, endDate, startDate, pageNo=1):
        search_json = {
            "areaJson": "",
            "bizMark": "",
            "buyerNick": "",
            "commentsRemarks": "",
            "customizeResidueSendTime": "",
            "startTime": startDate,
            "endTime": endDate,
            "equalFlag": 1,
            "exceptionFlag": "",
            "flagValue": "",
            "goodStockStatus": "",
            "goodsContain": False,
            "goodsTotalNum": "0-999999999",
            "goodsTypeNum": "0-999999999",
            "isFirstSend": False,
            "isPrecise": False,
            "isPreciseByTrade": False,
            "mobile": "",
            "multiShopS": stores,
            "orderRange": "0-999999999",
            "pageNo": pageNo,
            "pageSize": 1000,
            "payment": "0-999999999",
            "printStatus": "",
            "receiveName": "",
            "selValue": "",
            "sellAttribute": "",
            "sellerFlag": "",
            "sellerMemo": "",
            "serviePromiseType": "",
            "sid": "",
            "smartSelectExpress": "",
            "status": "ALL_STATUS",
            "testStatus": 0,
            "tid": "",
            "timeType": "1",
            "tradeExpressImportLogSequence": None,
            "weightRange": "0-999999999"
        }
        response = self.spyder.post(self.search_url, json=search_json, headers=self.headers)
        if response.status_code == 200 and pageNo == 1:
            data = response.json()
            return {'status': 'success', 'message': "正在获取订单", "data": data, "total": data["data"]["totalCount"]}
        elif pageNo != 1:
            data = response.json()
            return {'status': 'success', 'message': "正在获取订单", "data": data, }
        else:
            return {'status': 'failed', 'message': "返回码：{}".format(response.status_code), "data": ""}

    def DealOrder(self, order_JSON):
        for order_info in order_JSON["data"]["data"]["list"]:
            parent_order = {
                "sellerId": order_info["sellerId"],
                "sellerNick": order_info["sellerNick"],
                "platform": order_info["platform"],
                "orderID": order_info["encodeTid"],
                "receiverProvince": order_info["receiverState"],
                "receiverCity": order_info["receiverCity"],
                "totalPayment": order_info["totalPayment"],
                "totalReceivedPayment": order_info["totalReceivedPayment"],
                "updateTime": order_info["createTime"],
                "payTime": order_info.get("payTime", None),
                'orders': []
            }
            for order in order_info["trades"][0]['orders']:
                order_dict = {
                    "code": order.get("outerSkuId") if order.get("outerSkuId") else order.get("title")[:20],
                    "SkuName": order.get("skuPropertiesName").replace("颜色分类:", "") if order.get(
                        "skuPropertiesName") else order.get("title", "")[:20],
                    "quantity": order["num"],
                    "orderID": order["oid"],
                    "title": order["title"],
                    "payment": order["payment"],
                    "refund": self.getRefundStatus(order["refundStatus"]),
                    "status": self.getStatus(order["status"]),
                    "express": order.get("ydNoStr", "").split(":")[0] if order.get("ydNoStr") else "",
                    "expressOrder": order.get("ydNoStr", "").split(":")[1] if order.get("ydNoStr") else "",
                }
                parent_order["orders"].append(order_dict)
            yield parent_order

    def getStatus(self, status):
        status_dict = {
            "WAIT_BUYER_PAY": "待付款",
            "WAIT_SELLER_SEND_GOODS": "待发货",
            "TRADE_CLOSED": "订单关闭",
            "WAIT_BUYER_CONFIRM_GOODS": "待收货",
            "TRADE_FINISHED": "交易成功"}
        return status_dict.get(status)

    def getRefundStatus(self, status):
        status_dict = {
            "REFUND_SUCCESSED": "退款成功",
            "NOT_REFUND": "未退款",
        }
        return status_dict.get(status) if status_dict.get(status) else "未退款"

    def getRefund(self, endDate, startDate, pageNo=1):
        refund_json = {
            "createTimeStart": startDate,
            "createTimeEnd": endDate,
            "pageNo": pageNo,
            "pageSize": 200,
            "sysItemInclude": True
        }
        response = self.spyder.post(self.refund_url, json=refund_json, headers=self.headers)
        if response.status_code == 200 and pageNo == 1:
            data = response.json()
            return {'status': 'success', 'message': "正在获取订单", "data": data, "total": data["data"]["total"]}
        elif pageNo != 1:
            data = response.json()
            return {'status': 'success', 'message': "正在获取订单", "data": data, }
        else:
            return {'status': 'failed', 'message': "返回码：{}".format(response.status_code), "data": ""}

    def dealRefund(self, refund_json):
        for order_info in refund_json["data"]["data"]["list"]:
            refund_order = {
                "tid": order_info["tid"],
                "refundId": order_info["refundId"],
                "sellerId": order_info["sellerId"],
                "code": order_info["refundItemRecordInfos"][0].get("outerSkuId") if order_info["refundItemRecordInfos"][
                    0].get("outerSkuId") else order_info["refundItemRecordInfos"][0].get("itemAlias")[:20],
                "SkuName": order_info["refundItemRecordInfos"][0].get("skuName").replace("颜色分类:",
                                                                                         "") if
                order_info["refundItemRecordInfos"][0].get(
                    "skuName") else order_info["refundItemRecordInfos"][0].get("itemAlias", "")[:20],
                "CreatedTime": order_info["refundCreatedTime"],
                "ModifiedTime": order_info["refundModifiedTime"],
                "Amount": order_info["refundAmount"],
                "reason": order_info["refundReason"],
                "StatusDesc": order_info["refundStatusDesc"],
            }
            yield refund_order

    def dealCreateOrder(self, order_json):
        order_list = []
        shipInfo = ''
        payment = 0
        for order in order_json['saleList']:
            orders = {
                "discount": "",
                "itemId": "",
                "num": order.get("number"),
                "numIid": "",
                "outerId": "",
                "outerSkuId": order.get("sale"),
                "payment": order.get("price"),
                "picPath": "",
                "price": "",
                "priceType": "1",
                "refundStatus": "",
                "shortTitle": "",
                "skuId": "",
                "skuName": order.get("name"),
                "sysItemId": "",
                "sysSkuId": "",
                "title": "",
                "weight": "0",
            }
            order_list.append(orders)
            shipInfo += order.get("name") + ":" + order.get("number") + "\n"
            payment += float(order.get("price")) * int(order.get("number"))
        return order_list, shipInfo, payment

    def addSaleProduct(self, brandId, classifyid, Aliax, SaleID, supplierId, weight, price):  #
        addSaleJson = {
            "brandId": brandId,
            "classifyId": classifyid,
            "sysItemAlias": Aliax,
            "sysItemSaveType": 0,
            "sysSkuList": [
                {
                    "autoCostPrice": 0,
                    "autoWeight": 0,
                    "enableStatus": 1,
                    "market": "",
                    "skuOuterId": SaleID,
                    "stall": "",
                    "supplierId": supplierId,
                    "weight": weight,
                    "price": price
                }
            ]
        }
        response = self.spyder.post(self.addSaleProduct_url, json=addSaleJson, headers=self.headers)
        print(response.json())

    def addBrand(self, newBrand):
        addBrand_json = {
            "brandName": newBrand,
            "id": ""
        }
        response = self.spyder.post(self.addBrand_url, json=addBrand_json, headers=self.headers)
        print(response.json())

    def addSupply(self):
        pass

    def gerStoreKDZS(self):
        store_json = {
            "refresh": 1,
            "userId": "1251533"}
        response = self.spyder.get(self.store_url, json=store_json, headers=self.headers)

        print(response)
        if response.status_code == 200 and response.json()["data"]:
            originaldata = response.json()['data']['list']
            data = [
                {
                    "sellerId": original["sellerId"],
                    "sellerNick": original["sellerNick"],
                    "sellerAbbreviation": original["sellerAbbreviation"],
                    "platform": original["platform"],
                    "bindTime": original["bindTime"],
                    "status": original["status"],

                }
                for original in originaldata]
            return {'status': 'success', 'message': "更新完毕", "data": data, }
        else:
            return {'status': 'failed', 'message': "返回码：{}".format(response.status_code), "data": ""}

    def uploadHandOrder(self, upload_path):
        files = {
            # 'file': ('excel模板.xls', open('../../static/excel/普通EXCEL模板.xls', 'rb'), 'application/vnd.ms-excel')
            'file': ('excel模板.xls', open(upload_path, 'rb'), 'application/vnd.ms-excel,')
        }
        data = {
            "sellerId": "1251533",
            'sellerNick': '无店铺',
            'platform': 'hand',
        }
        upload_excel_result = self.spyder.post(self.hand_order_url, data=data, files=files, headers=self.headers)
        if upload_excel_result.status_code == 200:
            if upload_excel_result.json()['success']:
                data = {"asyncCode": upload_excel_result.json()['data']['cacheKey']}
                progress_result = self.spyder.post(self.progress_url, json=data, headers=self.headers)
                print(progress_result.json())
                if progress_result.json()['success']:
                    return {"status": "success", "message": "上传成功"}
                else:
                    return {"status": "failed", "message": "上传订单失败"}

            else:
                errorMessage = upload_excel_result.json()['errorMessage']
                return {"status": "failed", "message": errorMessage}

        else:
            return {"status": "failed", "message": "上传手工单失败，请查看令牌是否过期"}


if __name__ == '__main__':
    ZS = KuaiDiZhuShouSpyder()
    orders = ZS.createTrade()
    # Status = ZS.TestCookie()
    # if Status["status"] == "OK":
    #     ZS.iuputOrder()
    # else:
    #     print(Status['message'])
