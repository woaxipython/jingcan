import os
from datetime import datetime, timedelta

import pandas as pd
from sqlalchemy import and_, cast, Date, extract, func, text

from models.back import AdMethodModel
from models.product import GroupModel, SaleModel
from models.store import OrderModel, ParentOrderModel, StoreModel, AdFeeModel, HandParentOrderModel


# 获取店铺推广费数据
def getStoreProFee(end_date="2049-12-12", interval=10000, store_id="all", status="付款订单", date=True):
    end_date = datetime.strptime(end_date, "%Y-%m-%d")
    start_date = end_date - timedelta(days=interval)

    store_sql, group_by = confirmStore(store_id)
    # 生成查询条件
    filters = [AdFeeModel.upload_time >= start_date, AdFeeModel.upload_time < end_date]
    filters.extend(store_sql)
    Fees = AdFeeModel.query.filter(*filters).join(AdFeeModel.store) \
        .with_entities(
        cast(AdFeeModel.upload_time, Date).label('date'),
        func.sum(AdFeeModel.fee).label('total'),
        StoreModel.name.label('store_name')
    ).group_by(
        *group_by
    ).all()
    return Fees


# 获取子订单数据
def getOrderData(end_date="2049-12-12", interval=10000, status="付款订单", store_id="all", count=False, express=False,
                 date=True):
    end_date = datetime.strptime(end_date, "%Y-%m-%d")
    start_date = end_date - timedelta(days=interval)

    store_sql, group_by = confirmStore(store_id)
    filters = [OrderModel.updateTime >= start_date, OrderModel.updateTime < end_date]

    entities = [cast(OrderModel.updateTime, Date).label('date'), StoreModel.name.label('store_name'),
                func.sum(OrderModel.payment).label('total'), func.count(OrderModel.updateTime).label('count')
                ]

    # 生成查询条件
    status_sql = orderStatus(status)
    filters.extend(store_sql)
    filters.extend(status_sql)
    orders = OrderModel.query.filter(*filters).join(OrderModel.parent_order).join(
        ParentOrderModel.store
    ).with_entities(*entities).group_by(*group_by).all()
    return orders


def getParentOrders(end_date="2049-12-12", interval=10000, store_id="all", status="付款订单", count=False,
                    express=False, date=True):
    end_date = datetime.strptime(end_date, "%Y-%m-%d")
    start_date = end_date - timedelta(days=interval)

    store_sql, group_by = confirmStore(store_id)

    filters = [ParentOrderModel.updateTime >= start_date, ParentOrderModel.updateTime < end_date]

    entities = [cast(ParentOrderModel.updateTime, Date).label('date'),
                StoreModel.name.label('store_name'),
                func.sum(ParentOrderModel.totalPayment).label('total'),
                func.count(ParentOrderModel.orderID).label('count')]

    if status == "未付款":
        status = ParentOrderModel.payTime == None
    else:
        status = ParentOrderModel.payTime != None
    filters.append(status)

    if express == "已发货":
        entities.append(func.count(ParentOrderModel.express).label('express'))
        filters.append(ParentOrderModel.express != "")
    elif express == "待发货":
        entities.append(func.count(ParentOrderModel.express).label('express'))
        filters.append(ParentOrderModel.express == "")
    filters.extend(store_sql)

    orders = ParentOrderModel.query.filter(*filters).join(ParentOrderModel.store).with_entities(*entities).group_by(
        *group_by).all()
    return orders


# 获取商品销售数据
def getGroupData(end_date="2049-12-12", interval=10000, store_id="all", status="付款订单", count=False, express=False,
                 date=True):
    end_date = datetime.strptime(end_date, "%Y-%m-%d")
    start_date = end_date - timedelta(days=interval)

    store_sql, group_by = confirmStoreGroup(store_id)
    filters = [OrderModel.updateTime >= start_date, OrderModel.updateTime < end_date]

    entities = [cast(OrderModel.updateTime, Date).label('date'), StoreModel.name.label('store_name'),
                GroupModel.name.label('group_name'), func.sum(OrderModel.payment).label('total'),
                func.count(OrderModel.updateTime).label('count')]

    # 生成查询条件
    status_sql = orderStatus(status)
    filters.extend(store_sql)
    filters.extend(status_sql)

    orders = OrderModel.query.filter(*filters).join(OrderModel.parent_order).join(
        ParentOrderModel.store).join(OrderModel.sale).join(SaleModel.group).with_entities(
        *entities).group_by(
        *group_by).all()
    return orders


# 获取父订单数据


# 获取地图数据
def getParentMap(end_date="2049-12-12", interval=10000, store_id="all", status="付款订单", city="province"):
    end_date = datetime.strptime(end_date, "%Y-%m-%d")
    start_date = end_date - timedelta(days=interval)
    filters = [ParentOrderModel.updateTime >= start_date, ParentOrderModel.updateTime < end_date, ]

    entities = [func.sum(ParentOrderModel.totalPayment).label('total'),
                func.count(ParentOrderModel.orderID).label('count'),
                ]
    entities.insert(0, ParentOrderModel.province.label('locality')) if city == "province" else entities.insert(0,
                                                                                                               ParentOrderModel.city.label(
                                                                                                                   'locality'))

    if store_id == "all":
        store_sql = [StoreModel.id != 0]
        group_by = ['locality']
        store_enty = []
    elif store_id == "0":
        store_sql = [StoreModel.id != 0]
        group_by = ['locality', 'store_name']
        store_enty = [StoreModel.name.label('store_name')]
    else:
        store_sql = [StoreModel.id == store_id]
        group_by = ['locality', 'store_name']
        store_enty = [StoreModel.name.label('store_name')]
    filters.extend(store_sql)
    entities.extend(store_enty)

    status = ParentOrderModel.payTime == None if status == "未付款" else ParentOrderModel.payTime != None
    filters.append(status)

    orders = ParentOrderModel.query.filter(*filters).join(ParentOrderModel.store).with_entities(*entities).group_by(
        *group_by).all()
    return orders


# 获取时间数据
def getParentTimeOrder(end_date="2049-12-12", interval=10000, store_id="all", status="付款订单", ):
    end_date = datetime.strptime(end_date, "%Y-%m-%d")
    start_date = end_date - timedelta(days=interval)
    filters = [ParentOrderModel.updateTime >= start_date, ParentOrderModel.updateTime < end_date, ]
    entities = [ParentOrderModel.updateTime.label('date'),
                func.sum(ParentOrderModel.totalPayment).label('total'),
                func.count(ParentOrderModel.orderID).label('count'),
                ]
    if store_id == "all":
        store_sql = [StoreModel.id != 0]
        group_by = ['date']
        store_enty = []
    elif store_id == "0":
        store_sql = [StoreModel.id != 0]
        group_by = ['date', 'store_name']
        store_enty = [StoreModel.name.label('store_name')]
    else:
        store_sql = [StoreModel.id == store_id]
        group_by = ['date', 'store_name']
        store_enty = [StoreModel.name.label('store_name')]
    filters.extend(store_sql)
    entities.extend(store_enty)
    status = ParentOrderModel.payTime == None if status == "未付款" else ParentOrderModel.payTime != None
    filters.append(status)

    orders = ParentOrderModel.query.filter(*filters).join(ParentOrderModel.store).with_entities(*entities).group_by(
        *group_by).all()
    return orders


# 获取店铺推广费数据
def getStoreFee(end_date="2049-12-12", interval=10000, store_id="all", date=True, group="all"):
    end_date = datetime.strptime(end_date, "%Y-%m-%d")
    start_date = end_date - timedelta(days=interval)
    filters = [AdFeeModel.upload_time >= start_date, AdFeeModel.upload_time < end_date, ]

    entities = [cast(AdFeeModel.upload_time, Date).label('date'),
                StoreModel.name.label('store_name'),
                AdMethodModel.name.label('method_name'),
                GroupModel.name.label('group_name'),
                func.sum(AdFeeModel.fee).label('total')]

    store_sql, group_by = confirmStore(store_id)
    group_by.extend(confirmGroup(group))
    group_by.append('method_name')
    filters.extend(store_sql)

    orders = ParentOrderModel.query.filter(*filters).join(AdFeeModel.store).join(AdFeeModel.admethod).join(
        AdFeeModel.group).with_entities(*entities).group_by(
        *group_by).all()
    return orders


# 获取手工单数据
def getHandOrderInfo(startDate="", endDate="", category="", status="", dis="", days=7):
    if startDate == "":
        startDate = datetime.now() - timedelta(days=days)
    if endDate == "":
        endDate = datetime.now()
    filters = [HandParentOrderModel.createTime >= startDate, HandParentOrderModel.createTime < endDate, ]
    if category and category != "0":
        filters.append(HandParentOrderModel.category_id == category)
    if status and status != "0":
        if status == "1":
            filters.append(HandParentOrderModel.status != "")
        elif status == "2":
            filters.append(HandParentOrderModel.status == "")
    if dis and dis != "0":
        filters.append(HandParentOrderModel.distributor_id == dis)
    orders = HandParentOrderModel.query.filter(*filters).all()
    return orders


# 确认店铺信息
def confirmStore(store_id):
    if store_id == "all":
        store_sql = [StoreModel.id != 0]
        group_by = ['date']
    elif store_id == "0":
        store_sql = [StoreModel.id != 0]
        group_by = ['date', 'store_name']
    else:
        store_sql = [StoreModel.id == store_id]
        group_by = ['date', 'store_name']
    return store_sql, group_by


def confirmStoreGroup(store_id):
    if store_id == "all":
        store_sql = [StoreModel.id != 0]
        group_by = ['date', 'store_name', 'group_name']
    elif store_id == "0":
        store_sql = [StoreModel.id != 0]
        group_by = ['date', 'store_name', 'group_name']
    else:
        store_sql = [StoreModel.id == store_id]
        group_by = ['date', 'store_name', 'group_name']
    return store_sql, group_by


# 确认产品分组
def confirmGroup(group):
    if group == "all":
        group_by = []
    elif group == "0":
        group_by = ['group_name']
    else:
        group_by = ['group_name']
    return group_by


def orderStatus(status="付款订单"):
    order_staus = {
        "未付款": [and_(OrderModel.status == "订单关闭", OrderModel.refund == "未退款")],
        "付款订单": [~and_(OrderModel.status == "订单关闭", OrderModel.refund == "未退款")],
        "仅退款": [
            and_(OrderModel.status == "订单关闭", OrderModel.refund == "退款成功", OrderModel.expressOrder == "")],
        "退货退款": [
            and_(OrderModel.status == "订单关闭", OrderModel.refund == "退款成功", OrderModel.expressOrder != "")],
        "退款订单": [and_(OrderModel.status == "订单关闭", OrderModel.refund == "退款成功")],
    }
    return order_staus.get(status) if order_staus.get(status) else ""


def makeStoreProFile(save_path):
    ad_model = AdMethodModel.query.all()
    column = ['平台', '推广方式', '当前店铺']
    ad_method = []
    writer = pd.ExcelWriter(save_path)

    # 生成推广模板
    columns2 = ["推广平台", "推广方式", "推广店铺", "推广商品", "推广花费", "推广时间"]
    df2 = pd.DataFrame(columns=columns2)
    df2.to_excel(writer, index=False, sheet_name="推广模板", )

    # 生成现有推广方式
    for ad in ad_model:
        for store in ad.plat.stores:
            plat = ad.plat.name
            ad_name = ad.name
            store = store.name
            ad_method.append([plat, ad_name, store])
    df = pd.DataFrame(ad_method, columns=column)
    df.to_excel(writer, index=False, sheet_name="现有推广方式")

    # 生成产品模板
    group = GroupModel.query.all()
    group_list = []
    for g in group:
        group_list.append(g.name)
    df3 = pd.DataFrame(group_list, columns=["产品名称"])
    df3.to_excel(writer, index=False, sheet_name="现有产品")

    writer.active = 0

    writer.close()
