import os
from datetime import datetime, timedelta
import xlwt
from flask import jsonify, current_app
from sqlalchemy import func, and_, or_

from APP.SQLAPP.addEdit.dataWrite import generate_Number_string
from APP.Spyder.KdzsSpyder import KuaiDiZhuShouSpyder
from APP.Spyder.getAddress import getAddress
from APP.createCodeId import createOrderCode
from exts import db
from models.back import PlatModel, AdMethodModel
from models.product import SaleModel, GroupModel
from models.store import StoreModel, ParentOrderModel, OrderModel, RefundModel, DistributionModel, HandOrderModel, \
    HandOrderCategory, HandParentOrderModel, AdFeeModel, CodeStractModel
from models.user import UserModel
import pandas as pd
from openpyxl.reader.excel import load_workbook

kdzs = KuaiDiZhuShouSpyder()


# 写入订单数据
class writeOrderData(object):
    def __init__(self, order_info):
        self.order_info = order_info
        self.store_id = self.order_info['sellerId']
        self.plat_store_name = self.order_info['sellerNick']
        self.store_name = self.order_info['sellerNick']
        self.orderID = self.order_info['orderID']
        self.province = self.order_info['receiverProvince']
        self.city = self.order_info['receiverCity']
        self.totalPayment = self.order_info['totalPayment']
        self.totalReceivedPayment = self.order_info['totalReceivedPayment']
        self.updateTime = self.order_info['updateTime']
        self.payTime = self.order_info['payTime']
        self.orders = self.order_info['orders']
        self.checkStore()
        self.checkParentOrder()
        self.writrOrder()

    def checkStore(self):
        self.store_model = StoreModel.query.filter_by(store_id=self.store_id).first()
        if not self.store_model:
            self.store_model = StoreModel(store_id=self.store_id, plat_store_name=self.plat_store_name,
                                          name=self.store_name)
        if self.store_name == "手工单":
            self.hand_order_model = HandParentOrderModel.query.filter_by(orderID=self.orderID).first()
        else:
            self.hand_order_model = None

    def checkParentOrder(self):
        self.parent_order_model = ParentOrderModel.query.filter_by(orderID=self.orderID).first()
        if not self.parent_order_model:
            self.parent_order_model = ParentOrderModel(orderID=self.orderID, province=self.province,
                                                       city=self.city,
                                                       totalPayment=self.totalPayment,
                                                       totalReceivedPayment=self.totalReceivedPayment,
                                                       updateTime=self.updateTime)
        else:
            self.parent_order_model.province = self.province
            self.parent_order_model.city = self.city
            self.parent_order_model.totalPayment = self.totalPayment
            self.parent_order_model.totalReceivedPayment = self.totalReceivedPayment
            self.parent_order_model.updateTime = self.updateTime
        self.parent_order_model.store = self.store_model
        self.parent_order_model.payTime = self.payTime

    def writrOrder(self):
        for order in self.orders:
            self.order_model = OrderModel.query.filter_by(orderID=order['orderID']).first()
            if not self.order_model:
                self.order_model = OrderModel(orderID=order['orderID'], code=order['code'], quantity=order['quantity'],
                                              payment=order['payment'], updateTime=self.updateTime,
                                              express=order['express'], expressOrder=order['expressOrder'])
            self.order_model.refund = order['refund']
            self.order_model.status = order['status']
            sale_pr_model = SaleModel.query.filter_by(code=order["code"]).first()
            if not sale_pr_model:
                constract_model = CodeStractModel.query.filter_by(name=order['SkuName']).first()
                if not constract_model:
                    constract_model = CodeStractModel(name=order['SkuName'], store=self.store_model)
                    sale_pr_model = SaleModel(sale_name=order['SkuName'])
                else:
                    sale_pr_model = constract_model.sale
                constract_model.sale = sale_pr_model

            sale_pr_model.store.append(self.store_model)
            self.parent_order_model.express = order['express']
            self.parent_order_model.expressOrder = order['expressOrder']
            self.parent_order_model.status = order['status']
            if self.hand_order_model:
                self.hand_order_model.status = order['status']
                self.hand_order_model.express = order['express']
                self.hand_order_model.expressOrder = order['expressOrder']
            self.order_model.sale = sale_pr_model
            self.order_model.cost = sale_pr_model.cost
            self.order_model.parent_order = self.parent_order_model
            db.session.add(self.order_model)
            db.session.commit()


def writeRefund(refund_result):
    refund_model = RefundModel.query.filter_by(refund_id=refund_result['refundId']).first()
    parent_model = ParentOrderModel.query.filter_by(orderID=refund_result['tid']).first()
    parent_model = ParentOrderModel(orderID=refund_result['tid']) if not parent_model else parent_model

    store_model = StoreModel.query.filter_by(store_id=refund_result['sellerId']).first()
    store_model = StoreModel(store_id=refund_result['sellerId']) if not store_model else store_model

    # 退款订单匹配商品
    sale_pr_model = SaleModel.query.filter_by(code=refund_result["code"]).first()
    if not sale_pr_model:
        constract_model = CodeStractModel.query.filter_by(name=refund_result['SkuName']).first()
        if not constract_model:
            constract_model = CodeStractModel(name=refund_result['SkuName'], store=store_model)
            sale_pr_model = SaleModel(sale_name=refund_result['SkuName'])
        else:
            sale_pr_model = constract_model.sale
        constract_model.sale = sale_pr_model
    sale_pr_model.store.append(store_model)

    if not refund_model:
        refund_model = RefundModel(refund_id=refund_result["refundId"],
                                   status=refund_result["StatusDesc"],
                                   reason=refund_result["reason"],
                                   amount=refund_result["Amount"],
                                   modifiedTime=refund_result["ModifiedTime"],
                                   updateTime=refund_result["CreatedTime"], )
    else:
        refund_model.status = refund_result["StatusDesc"]
        refund_model.amount = refund_result["Amount"]
        refund_model.modifiedTime = refund_result["ModifiedTime"]
        refund_model.updateTime = refund_result["CreatedTime"]
        refund_model.reason = refund_result["reason"]
    refund_model.sale_id = sale_pr_model.id
    refund_model.parent_order = parent_model
    refund_model.store = store_model
    db.session.add(refund_model)
    db.session.commit()


def writeStore(store_list):
    new_store = []
    for store in store_list:
        store_id = store['sellerId']
        store_model = StoreModel.query.filter_by(store_id=store_id).first()
        if not store_model:
            store_model = StoreModel(name=store['sellerAbbreviation'],
                                     store_id=store_id,
                                     plat_store_name=store['sellerNick'],
                                     bindTime=store['bindTime'],
                                     status=True if store['status'] == 1 else False,
                                     )
            new_store.append(store['sellerAbbreviation'])
        else:
            store_model.name = store['sellerAbbreviation']
            store_model.plat_store_name = store['sellerNick']
            store_model.bindTime = store['bindTime']
            store_model.status = True if store['status'] == 1 else False

        plat_name = PlatNameZH(store['platform'].upper())
        plat_model = PlatModel.query.filter_by(name=plat_name).first()
        if not plat_model:
            plat_model = PlatModel(name=plat_name, EH_name=store['platform'], is_Store=True)
        store_model.plat = plat_model
        db.session.add(store_model)
        db.session.commit()
    return new_store


def PlatNameZH(EHname):
    name_dict = {"PDD": "拼多多", "TB": "淘宝", "FXG": "抖音", "JD": "京东", "KSXD": "快手", "OTHER": "其它"}
    return name_dict.get(EHname)


def writeAdMethodModel(form_dict):
    plat_model = PlatModel.query.get(form_dict.get("platName"))
    if plat_model:
        ad_method_model = AdMethodModel.query.filter_by(name=form_dict.get("proName")).first()
        if ad_method_model:
            return jsonify({"status": "failed", "message": "推广方式已存在"})
        else:
            ad_method_model = AdMethodModel(name=form_dict.get("proName"), plat_id=plat_model.id,
                                            desc=form_dict.get("proFeeModel"))
            db.session.add(ad_method_model)
            db.session.commit()
            return jsonify({"status": "success", "message": "新增成功"})
    else:
        return jsonify({"status": "failed", "message": "平台不存在"})


def writeNewDisModel(form_dict):
    user_model = UserModel.query.get(form_dict.get("newDisUser"))
    if not user_model:
        return jsonify({"status": "failed", "message": "没有该联络人"})
    else:
        dis_model = DistributionModel.query.filter_by(campany_name=form_dict.get("newDisCampany")).first()
        if dis_model:
            return jsonify({"status": "failed", "message": "分销公司已存在"})
        else:
            dis_model = DistributionModel(campany_name=form_dict.get("newDisCampany"), name=form_dict.get("newDisName"),
                                          wechat=form_dict.get("newDisWechat"),
                                          channel=form_dict.get("newDisSaleChannel"),
                                          phone=form_dict.get("newDisPhone"), city=form_dict.get("newDisCity"),
                                          province=form_dict.get("newDisProvince"), link=form_dict.get("newDisLink"),
                                          address=form_dict.get("newDisAddress"), remark=form_dict.get("newDisRemark"))
            dis_model.user = user_model
            db.session.add(dis_model)
            db.session.commit()
            return jsonify({"status": "success", "message": "新增成功"})


def writeHandOrder(form_dict):
    order_list, shipInfo, payment = kdzs.dealCreateOrder(form_dict)
    max_id = db.session.query(func.max(HandParentOrderModel.id)).scalar() or 0
    search_id = createOrderCode(max_id + 1)
    create_handle_order = kdzs.createTrade(form_dict=form_dict, order_list=order_list, shipInfo=shipInfo,
                                           search_id=search_id)
    if not create_handle_order['status']:
        return jsonify({"status": "success", "message": "创建订单失败"})
    hands_type = HandOrderCategory.query.get(form_dict['handOrderModel'])
    if not hands_type:
        return jsonify({"status": "failed", "message": "没有该订单类型"})
    handorder_model = HandParentOrderModel(search_id=search_id, province=form_dict['handOrderProvince'],
                                           city=form_dict['handOrderCity'], address=form_dict['handOrderAddress'],
                                           phone=form_dict['handOrderPhone'], name=form_dict['handOrderName'],
                                           payment=payment,
                                           remark=form_dict['handOrderRemark']
                                           )
    user_model = UserModel.query.get(form_dict['handOrderUser'])
    order_category = HandOrderCategory.query.get(form_dict['handOrderModel'])
    handorder_model.user = user_model
    handorder_model.category = order_category
    for order in order_list:
        order_model = HandOrderModel(code=order['outerSkuId'], quantity=order['num'], payment=order['payment'])
        sale_model = SaleModel.query.filter_by(code=order['outerSkuId']).first()
        if not sale_model:
            sale_model = SaleModel(name=order['skuName'], code=order['outerSkuId'])
        order_model.sale = sale_model
        order_model.cost = sale_model.cost
        order_model.hand_parent_order = handorder_model
        db.session.add(order_model)
    db.session.add(handorder_model)
    db.session.commit()
    return jsonify({"status": "success", "message": "创建订单成功"})


class WriteExcelOrder(object):
    def __init__(self, form_dict, save_path):
        self.form_dict = form_dict
        self.save_path = save_path
        self.upload_path = 'static/excel/普通EXCEL模板.xls'
        self.user = self.form_dict.get('disOrderUser')
        self.dis = self.form_dict.get('disOrderName')

    def check(self):
        self.user_model = UserModel.query.get(self.user)
        if not self.user_model:
            return False
        self.dis_model = DistributionModel.query.get(self.dis)
        if not self.dis_model:
            return False
        return True

    def makeKdzsExcel(self):
        workbook = load_workbook(self.save_path)
        sheet = workbook['分销商订单模板']
        max_id = db.session.query(func.max(HandParentOrderModel.id)).scalar() or 0
        search_id = createOrderCode(max_id + 1)
        self.order_lists = []

        columns = ["订单编号", "*收件人", "固话", "*手机", "*地址", "发货信息", "*货品规格编码", "宝贝数量", "总重量",
                   "备注", "代收货款(是/否)", "保价服务(是/否)", "实付金额"]
        self.order_lists.append(columns)
        for row in sheet.rows:
            if row[0].row == 1:
                continue
            order_list = []
            name = row[0].value
            sale_model = SaleModel.query.filter_by(name=name).first()
            if not sale_model:
                return {"status": "failed", "message": "没有第{}行产品，请重新填写".format(row[0].column)}
            order_list.append(search_id)
            order_list.append(row[3].value)
            order_list.append("")
            order_list.append(row[4].value)
            order_list.append(row[5].value)
            order_list.append(name + ':' + str(row[1].value) + "只")
            order_list.append(sale_model.code)
            order_list.append(row[1].value)
            order_list.append("")
            order_list.append("")
            order_list.append("")
            order_list.append("")
            order_list.append(row[2].value)
            self.order_lists.append(order_list)
            search_id = "O" + str(int(search_id[1:]) + 1)
        workbook.close()
        wb = xlwt.Workbook()
        ws = wb.add_sheet('sheet1')
        i = 0
        for row in self.order_lists:
            j = 0
            for col in row:
                ws.write(i, j, col)
                j += 1
            i += 1
        wb.save(self.upload_path)
        return {"status": "success", "message": "生成成功"}

    def uploadExcelFile(self):
        result = kdzs.uploadHandOrder(upload_path=self.upload_path)
        print(result)
        if result['status'] == "failed":
            return {"status": "failed", "message": result['message']}
        else:
            return {"status": "success", "message": "上传成功"}

    def writeHandOrder(self):
        for order_list in self.order_lists:
            user_model = UserModel.query.get(self.form_dict['disOrderUser'])
            order_category = HandOrderCategory.query.filter_by(name="分销商订单").first()
            if not order_category:
                order_category = HandOrderCategory(name="分销商订单")
            handorder_model = HandParentOrderModel(search_id=order_list[0], address=order_list[4],
                                                   payment=order_list[12],
                                                   name=order_list[1], phone=order_list[3],
                                                   )
            handorder_model.user = user_model
            handorder_model.category = order_category
            order_model = HandOrderModel(code=order_list[6], quantity=order_list[7], payment=order_list[12])
            sale_model = SaleModel.query.filter_by(code=order_list[6]).first()
            order_model.sale = sale_model
            order_model.hand_parent_order = handorder_model
            db.session.add(order_model)
            db.session.add(handorder_model)
        db.session.commit()
        return {"status": "success", "message": "创建订单成功"}


def writeStorePromotionFee(form_dict):
    error_message = []
    for Ad in form_dict['AdList']:
        write_result = writeStoreFee(Ad)
        if write_result['status'] == "failed":
            error_message.append(write_result['message'])
            continue
    if error_message:
        return jsonify({"status": "failed", "message": error_message})
    else:
        return jsonify({"status": "success", "message": "新增成功"})


def writeStorePromotionFile(save_path):
    workbook = load_workbook(save_path)
    sheet = workbook.active
    error_message = []
    for row in sheet.rows:
        if row[0].row == 1:
            continue
        print(row[0].value)
        plat_model = PlatModel.query.filter_by(name=row[0].value).first()
        if not plat_model:
            error_message.append("第" + str(row[0]) + "列的平台不存在")
            continue
        plat_id = plat_model.id
        method_model = AdMethodModel.query.filter_by(plat_id=plat_id, name=row[1].value).first()
        if not method_model:
            error_message.append("第" + str(row[1].column) + "列的广告方式不存在")
            continue
        method_id = method_model.id
        store_model = StoreModel.query.filter_by(name=row[2].value).first()
        if not store_model:
            error_message.append("第" + str(row[2].column) + "列的店铺不存在")
            continue
        store_id = store_model.id
        group_model = GroupModel.query.filter_by(name=row[3].value).first()
        if not group_model:
            error_message.append("第" + str(row[3].column) + "列的商品组不存在")
            continue
        group_id = group_model.id
        Ad = {'plat': plat_id, 'method': method_id, 'store': store_id, 'product': group_id, 'fee': row[4].value,
              'date': row[5].value, }
        write_result = writeStoreFee(Ad)
        if write_result['status'] == "failed":
            error_message.append(write_result['message'])
            continue
    if error_message:
        return jsonify({"status": "failed", "message": error_message})
    else:
        return jsonify({"status": "success", "message": "新增成功"})


def writeStoreFee(Ad):
    plat = Ad['plat']
    method = Ad['method']
    store = Ad['store']
    product = Ad['product']
    ad_model = AdMethodModel.query.filter_by(plat_id=plat, id=method).first()
    if not ad_model:
        return {"status": "failed", "message": "广告方式不存在"}
    store_model = StoreModel.query.filter_by(id=store).first()
    if not store_model:
        return {"status": "failed", "message": "店铺不存在"}
    product_model = GroupModel.query.filter_by(id=product).first()
    if not product_model:
        return {"status": "failed", "message": "商品组不存在"}
    maxid = db.session.query(func.max(AdFeeModel.id)).scalar() or 0 + 1
    search_id = datetime.now().strftime('%Y-%m-%d') + "-" + generate_Number_string(6, maxid)
    fee_model = AdFeeModel.query.filter_by(search_id=search_id).first()
    if not fee_model:
        fee_model = AdFeeModel(search_id=search_id)
    fee_model.admethod = ad_model
    fee_model.store = store_model
    fee_model.group = product_model
    fee_model.upload_time = Ad['date']
    fee_model.fee = Ad['fee']
    db.session.add(fee_model)
    db.session.commit()
    return {"status": "success", "message": "新增成功"}
