import pandas as pd
from flask import jsonify

from APP.Spyder.DySpyder import DouYinSpyder
from APP.Spyder.XshSpyder import GetXhsSpyder
from models.product import AtomModel, SaleModel, GroupModel

xhs = GetXhsSpyder()
dy = DouYinSpyder()


def searchAtomModel(name, category_id):
    if not name and category_id == "all":
        atoms = AtomModel.query.all()
    elif name and category_id == "all":
        name = '%{}%'.format(name)
        atoms = AtomModel.query.filter(AtomModel.name.like(name)).all()
    elif not name and not category_id:
        atoms = AtomModel.query.all()
    elif not name and category_id:
        atoms = AtomModel.query.filter_by(category_id=category_id).all()
    else:
        atoms = AtomModel.query.filter(AtomModel.name == name, AtomModel.category_id == category_id).all()
    return atoms


def searchSaleModel(name, saleC):
    if not name and saleC == "all":
        sales = SaleModel.query.all()
    elif name and saleC == "all":
        name = '%{}%'.format(name)
        sales = SaleModel.query.filter(SaleModel.name.like(name)).all()
    elif not name and saleC == "0":
        sales = SaleModel.query.filter(SaleModel.name == None).all()
    elif name and saleC == "0":
        name = '%{}%'.format(name)
        sales = SaleModel.query.filter(SaleModel.name.like(name)).all()
    elif not name and saleC == "1":
        sales = SaleModel.query.filter(SaleModel.name != None).all()
    elif name and saleC == "1":
        name = '%{}%'.format(name)
        sales = SaleModel.query.filter(SaleModel.name.like(name)).all()
    else:
        sales = SaleModel.query.all()
    return sales


def refreshSaleFile():
    sale_list = SaleModel.query.all()
    column = ["销售名称", "商品简称(打单名称)", "商品编码", "售价", '店铺', "创建时间"]
    sale_info = []
    for sale in sale_list:
        sale_name = sale.sale_name
        name = sale.name
        code = sale.code
        price = sale.price
        store = ".".join([store.name for store in sale.store])
        create_time = sale.createtime
        sale_list = [name, sale_name, code, price, store, create_time]
        sale_info.append(sale_list)
    df = pd.DataFrame(sale_info, columns=column)
    df.to_excel("static/excel/sale.xlsx", index=False)
    return jsonify({"status": "success", "message": "导出成功"})


def downLoadDisFile(save_path):
    writer = pd.ExcelWriter(save_path)

    column2 = ["商品名称", "商品数量", "商品单价", "收件人", "收件人电话", "收件人地址"]
    df2 = pd.DataFrame(columns=column2)
    df2.to_excel(writer, index=False, sheet_name="分销商订单模板")

    sale_list = SaleModel.query.all()
    column = ["销售名称", "商品简称(打单名称)", "商品编码", "售价", "创建时间"]
    sale_info = []
    for sale in sale_list:
        if sale.name:
            sale_name = sale.sale_name
            name = sale.name
            code = sale.code
            price = sale.price
            create_time = sale.createtime
            sale_list = [name, sale_name, code, price, create_time]
            sale_info.append(sale_list)
    df = pd.DataFrame(sale_info, columns=column)
    df.to_excel(writer, index=False, sheet_name="现有商品明细")

    writer.active = 0
    writer.close()
    return jsonify({"status": "success", "message": "导出成功"})


def makeHandOrderExcel(save_path, order_list):
    writer = pd.ExcelWriter(save_path)
    columns = ["手工单编号", "商品简称", "商品数量", "商品单价", "收件人", "收件人电话", "收件人地址", "创建时间",
               "分销商", "快递单号"]
    order_info = []
    for orders in order_list:
        for order in orders:
            order_id = order.search_id
            name = order.sale.name
            number = order.quantity
            price = order.payment
            receiver = orders.name
            phone = orders.phone
            address = orders.address
            create_time = orders.create_time
            distributor = orders.distribution.name if orders.distribution else ""
            exepress = orders.expressOrder
            order_list = [order_id, name, number, price, receiver, phone, address, create_time, distributor, exepress]
            order_info.append(order_list)

    df = pd.DataFrame(order_info, columns=columns)
    df.to_excel(writer, index=False, sheet_name="手工单明细")
    writer.active = 0
    writer.close()
    return {"status": "success", "message": "导出成功"}


def searchGroupModel(name):
    if not name:
        groups = GroupModel.query.all()
    else:
        name = '%{}%'.format(name)
        groups = GroupModel.query.filter(GroupModel.name.like(name)).all()
    return groups


def makeCodeStractFile(save_path):
    writer = pd.ExcelWriter(save_path)

    # 生成推广模板
    columns2 = ["销售名称", "商品编码"]
    df = pd.DataFrame(columns=columns2)
    df.to_excel(writer, index=False, sheet_name="推广模板", )

    # 生成商品模板
    sale_list = SaleModel.query.all()
    column = ["销售名称", "商品简称(打单名称)", "商品编码", "售价", '店铺', "创建时间"]
    sale_info = []
    for sale in sale_list:
        sale_name = sale.sale_name
        name = sale.name
        code = sale.code
        price = sale.price
        store = ".".join([store.name for store in sale.store])
        create_time = sale.createtime
        sale_list = [name, sale_name, code, price, store, create_time]
        sale_info.append(sale_list)
    df = pd.DataFrame(sale_info, columns=column)
    df.to_excel(writer, index=False, sheet_name="商品模板")

    writer.close()
