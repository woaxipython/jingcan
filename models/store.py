from shortuuid import uuid
from datetime import datetime
from enum import Enum

from exts import db


class ParentOrderModel(db.Model):
    __tablename__ = 'parent_order'
    id = db.Column(db.Integer, primary_key=True)
    search_id = db.Column(db.String(100), default=uuid)
    orderID = db.Column(db.String(50), nullable=False, unique=True)
    province = db.Column(db.String(30))
    city = db.Column(db.String(30))

    totalPayment = db.Column(db.Float, )
    totalReceivedPayment = db.Column(db.Float, )
    status = db.Column(db.String(30))
    express = db.Column(db.String(30))
    expressOrder = db.Column(db.String(30))

    updateTime = db.Column(db.DateTime)
    payTime = db.Column(db.DateTime)
    createTime = db.Column(db.DateTime, default=datetime.now)

    store_id = db.Column(db.Integer, db.ForeignKey("store.id"))
    store = db.relationship("StoreModel", backref="parent_orders")


# 子订单关系
class OrderModel(db.Model):
    __tablename__ = "order"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    search_id = db.Column(db.String(100), default=uuid)
    orderID = db.Column(db.String(50), nullable=False, unique=True)
    code = db.Column(db.String(30))
    quantity = db.Column(db.Integer)
    cost = db.Column(db.Float)
    refund = db.Column(db.String(30))
    status = db.Column(db.String(30))

    payment = db.Column(db.Float)
    payment_img = db.Column(db.String(50))

    express = db.Column(db.String(30))
    expressOrder = db.Column(db.String(30))

    updateTime = db.Column(db.DateTime)
    createTime = db.Column(db.DateTime, default=datetime.now)

    sale_id = db.Column(db.Integer, db.ForeignKey("sale.id"))
    sale = db.relationship("SaleModel", backref="orders")

    parent_order_id = db.Column(db.Integer, db.ForeignKey("parent_order.id"))
    parent_order = db.relationship("ParentOrderModel", backref="orders")


class StoreModel(db.Model):
    __tablename__ = 'store'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    search_id = db.Column(db.String(100), default=uuid)
    name = db.Column(db.String(50), nullable=False, unique=False)
    plat_store_name = db.Column(db.String(50), nullable=False, unique=False)
    store_id = db.Column(db.String(30))
    status = db.Column(db.Boolean, default=True)
    bindTime = db.Column(db.DateTime)
    createTime = db.Column(db.DateTime, default=datetime.now)

    # 店铺与平台之间的关系，一个平台，多个店铺
    plat_id = db.Column(db.Integer, db.ForeignKey('plat.id'))
    plat = db.relationship("PlatModel", backref='stores')

    # 店铺与品牌之间的关系，一个品牌多个店铺，一个店铺对应1个品牌
    brand_id = db.Column(db.Integer, db.ForeignKey('brand.id'))
    brand = db.relationship("BrandModel", backref='stores')

    # 一个运营专员可以对应多个店铺
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship("UserModel", backref='stores')


# 店铺广告费用
class AdFeeModel(db.Model):
    __tablename__ = "adfee"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    search_id = db.Column(db.String(100), default=uuid)
    fee = db.Column(db.Float, nullable=False)
    upload_time = db.Column(db.DateTime)
    create_time = db.Column(db.DateTime, default=datetime.now)

    admethod_id = db.Column(db.Integer, db.ForeignKey('admethod.id'))
    admethod = db.relationship("AdMethodModel", backref='adfees')

    group_id = db.Column(db.Integer, db.ForeignKey('group.id'))
    group = db.relationship("GroupModel", backref='adfees')

    store_id = db.Column(db.Integer, db.ForeignKey('store.id'))
    store = db.relationship("StoreModel", backref='adfees')


class RefundModel(db.Model):
    __tablename__ = "refund"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    search_id = db.Column(db.String(100), default=uuid)
    refund_id = db.Column(db.String(30), nullable=False)
    status = db.Column(db.String(30))
    amount = db.Column(db.Float)
    reason = db.Column(db.String(30))

    modifiedTime = db.Column(db.DateTime)
    updateTime = db.Column(db.DateTime)
    createTime = db.Column(db.DateTime, default=datetime.now)

    sale_id = db.Column(db.Integer, db.ForeignKey("sale.id"))
    sale = db.relationship("SaleModel", backref="refunds")

    store_id = db.Column(db.Integer, db.ForeignKey('store.id'))
    store = db.relationship("StoreModel", backref='refunds')

    parent_order_id = db.Column(db.Integer, db.ForeignKey("parent_order.id"))
    parent_order = db.relationship("ParentOrderModel", backref="refunds")


class HandParentOrderModel(db.Model):
    __tablename__ = "hand_parent_order"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    search_id = db.Column(db.String(100), default=uuid)

    province = db.Column(db.String(30))
    city = db.Column(db.String(30))
    address = db.Column(db.String(100))
    phone = db.Column(db.String(20))
    name = db.Column(db.String(20))
    payment = db.Column(db.Float, default=0)
    status = db.Column(db.String(20))
    express = db.Column(db.String(30))
    expressOrder = db.Column(db.String(30))
    remark = db.Column(db.String(100))
    createTime = db.Column(db.DateTime, default=datetime.now)

    category_id = db.Column(db.Integer, db.ForeignKey("hand_category.id"))
    category = db.relationship("HandOrderCategory", backref="hand_parent_orders")

    distribution_id = db.Column(db.Integer, db.ForeignKey("distribution.id"))
    distribution = db.relationship("DistributionModel", backref="hand_parent_orders")

    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    user = db.relationship("UserModel", backref="hand_parent_orders")


class CodeStractModel(db.Model):
    __tablename__ = "code_stract"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    store_title = db.Column(db.String(200))
    search_id = db.Column(db.String(100), default=uuid)
    name = db.Column(db.String(30))
    store_id = db.Column(db.Integer, db.ForeignKey("store.id"))
    store = db.relationship("StoreModel", backref="code_stracts")

    sale_id = db.Column(db.Integer, db.ForeignKey("sale.id"))
    sale = db.relationship("SaleModel", backref="code_stracts")
    createTime = db.Column(db.DateTime, default=datetime.now)


class HandOrderModel(db.Model):
    __tablename__ = "hand_order"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    search_id = db.Column(db.String(100), default=uuid)
    code = db.Column(db.String(30))
    quantity = db.Column(db.Integer)
    refund = db.Column(db.String(30))
    cost = db.Column(db.Float)
    status = db.Column(db.String(30))

    payment = db.Column(db.Float)
    payment_img = db.Column(db.String(50))

    express = db.Column(db.String(30))
    expressOrder = db.Column(db.String(30))

    sale_id = db.Column(db.Integer, db.ForeignKey("sale.id"))
    sale = db.relationship("SaleModel", backref="hand_orders")

    hand_parent_order_id = db.Column(db.Integer, db.ForeignKey("hand_parent_order.id"))
    hand_parent_order = db.relationship("HandParentOrderModel", backref="hand_orders")


class HandOrderCategory(db.Model):
    __tablename__ = "hand_category"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    search_id = db.Column(db.String(100), default=uuid)
    name = db.Column(db.String(50), nullable=False, unique=True)
    createTime = db.Column(db.DateTime, default=datetime.now)


class DistributionModel(db.Model):
    __tablename__ = "distribution"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    search_id = db.Column(db.String(100), default=uuid)
    name = db.Column(db.String(50), nullable=False, unique=True)
    campany_name = db.Column(db.String(50))
    phone = db.Column(db.String(20))
    wechat = db.Column(db.String(20))
    channel = db.Column(db.String(50))
    city = db.Column(db.String(30))
    province = db.Column(db.String(30))
    address = db.Column(db.String(100))
    link = db.Column(db.String(100))
    remark = db.Column(db.String(100))
    createTime = db.Column(db.DateTime, default=datetime.now)

    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    user = db.relationship("UserModel", backref="distributions")

class kdzsTokenModel(db.Model):
    __tablename__ = "kdzs_token"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    token = db.Column(db.String(300))
    name = db.Column(db.String(100))
    createTime = db.Column(db.DateTime, default=datetime.now)