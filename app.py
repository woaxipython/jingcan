# -*- coding: utf-8 -*-
from datetime import datetime

from flask import Flask, render_template, jsonify
from flask_migrate import Migrate
from sqlalchemy import and_

import command
import config
from APP.SQLAPP.makePandas.orderStore import makeOrderFrameData, makePOrderAll, mergeFrame, makePOrderStore
from APP.SQLAPP.search.orderStore import getOrderData, getStoreProFee, getParentOrders
from exts import db, mail, cache
from bbs_celery import make_celery
from flask_wtf import CSRFProtect
from blueprints.sale.saleManage import bp as sale_bp
from blueprints.promotionManage import bp as prm_bp
from blueprints.promotionData import bp as prd_bp
from blueprints.handOrderManage import bp as hd_bp
from blueprints.back.backManage import bp as bk_bp
from blueprints.back.product import bp as pr_bp
from blueprints.back.permission import bp as per_bp
from blueprints.back.user import bp as user_bp
from blueprints.back.store import bp as store_bp
from models.store import ParentOrderModel

app = Flask(__name__)

# config初始化
app.config.from_object(config.ProductiongConfig)

# SQlAlchemy初始化
db.init_app(app=app)

# Mail初始化，发送邮件
mail.init_app(app=app)

# Cache初始化，缓存验证码
cache.init_app(app=app)

# 引入Migrate插件，实现创建数据库
migrate = Migrate(app=app, db=db)

# 构建celery,异步执行
celery = make_celery(app=app)

# # 创建CSRF保护
CSRFProtect(app=app)

# 注册蓝图
app.register_blueprint(sale_bp)
app.register_blueprint(prm_bp)
app.register_blueprint(prd_bp)
app.register_blueprint(hd_bp)
app.register_blueprint(bk_bp)
app.register_blueprint(pr_bp)
app.register_blueprint(per_bp)
app.register_blueprint(user_bp)
app.register_blueprint(store_bp)

# 绑定command命令
app.cli.command("baseSelectModel")(command.baseSelectModel)


# app.cli.command("create-blogger")(command.create_blogger)


@app.route('/')
def index():  # put application's code here

    return render_template("index.html")


@app.route('/allToadyData')
def allToadyData():
    today_payment = getParentOrders(status="付款订单", end_date=datetime.now().date().strftime("%Y-%m-%d"), interval=1,
                                    count=1)
    today_wait = getParentOrders(status="未付款", end_date=datetime.now().date().strftime("%Y-%m-%d"), interval=1,
                                 count=1)
    today_express_d = ParentOrderModel.query.filter(ParentOrderModel.express != "").count()
    today_express_w = ParentOrderModel.query.filter(and_(ParentOrderModel.express == "",
                                                         ParentOrderModel.payTime != None)).count()
    print(today_express_w)
    today_refund = getOrderData(status="退款订单", end_date=datetime.now().date().strftime("%Y-%m-%d"), interval=1)
    today_store_pro = getStoreProFee(end_date=datetime.now().date().strftime("%Y-%m-%d"), interval=1)

    try:
        today_refund_payment = round(today_refund[0].count, 0)
    except:
        today_refund_payment = 0
    try:
        today_express_w = round(today_express_w, 0)
    except:
        today_express_w = 0
    try:
        today_express_d = round(today_express_d, 0)
    except:
        today_express_d = 0
    try:
        today_payment_orders = round(today_payment[0].total, 0)
        today_order_count = round(today_payment[0].count, 0)
    except:
        today_payment_orders = 0
        today_order_count = 0
    try:
        today_wait_orders = round(today_wait[0].count, 0)
    except:
        today_wait_orders = 0
    try:
        today_store_pro = round(today_store_pro[0].total, 0)
    except:
        today_store_pro = 0

    month_orders = getParentOrders(status="付款订单", end_date=datetime.now().date().strftime("%Y-%m-%d"),
                                   interval=40, store_id="0", count=1)
    month_orders = makePOrderAll(month_orders, cycle="M", store="0")
    month_orders = month_orders.iloc[1::2, :]
    month_orders["total"] = month_orders["total"].round(0)
    month_orders = month_orders.values.tolist()

    month_payment = round(sum(month[2] for month in month_orders), 0)
    month_orders_num = round(sum(month[3] for month in month_orders), 0)
    return jsonify(today_payment_orders=today_payment_orders, today_refund_payment=today_refund_payment,
                   today_store_pro=today_store_pro, today_order_count=today_order_count,
                   today_wait_orders=today_wait_orders, today_express_d=today_express_d,
                   today_express_w=today_express_w, month_payment=month_payment,
                   month_orders_num=month_orders_num)


@app.route('/orderData')
def orderData():
    payment_orders = getOrderData(status="付款订单")
    payment_orders = makeOrderFrameData(payment_orders, cycle="D")
    print(payment_orders.columns)

    refund_orders = getOrderData(status="退款订单")
    refund_orders = makeOrderFrameData(refund_orders, cycle="D")
    print(refund_orders.columns)
    order_refund = round(mergeFrame(payment_orders, refund_orders, type='date'), 0)
    print(order_refund)
    print(order_refund.columns)
    order_refund = order_refund.T.values.tolist()
    print(order_refund)

    return jsonify(order_refund)


@app.route('/pOrderData')
def pOrderData():
    parent_order = getParentOrders(count=1)
    parent_order = round(makePOrderAll(parent_order, cycle="D"), 0)
    parent_order = parent_order.T.values.tolist()
    return jsonify(parent_order)


@app.route('/storeProData')
def storeProData():
    month_orders = getParentOrders(status="付款订单", end_date=datetime.now().date().strftime("%Y-%m-%d"),
                                   interval=40, store_id="0", count=1)
    month_orders = makePOrderStore(month_orders, cycle="M", )
    month_orders = month_orders.T
    del month_orders[0]
    month_orders = month_orders.reset_index()
    month_orders.columns = ["store", "total"]
    month_orders.drop(month_orders.index[0], inplace=True)
    month_orders = month_orders.sort_values(by="total", ascending=False)

    month_orders = month_orders.values.tolist()

    return jsonify(month_orders)


if __name__ == '__main__':
    app.run()
