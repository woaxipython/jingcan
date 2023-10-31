import pandas as pd
from flask import jsonify

from APP.Spyder.DySpyder import DouYinSpyder
from APP.Spyder.XshSpyder import GetXhsSpyder
from models.product import AtomModel, SaleModel, GroupModel
from models.store import CodeStractModel

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
    from openpyxl import Workbook
    from openpyxl.utils import get_column_letter
    from openpyxl.worksheet.datavalidation import DataValidation

    # 创建一个新的工作簿
    wb = Workbook()
    sheet = wb.active

    sheet.title = "手工单模板"

    # 指定标题行的内容
    title_row = ["订单分类", "发货原因(分销则写分销商名称)", "商品名称", "商品数量", "商品单价", "收件人地址",
                 "下单时间", "快递公司", "快递单号"]
    sheet.append(title_row)

    # 指定下拉框的选项
    dropdown_values = ['手工单', '分销商']

    f = f'"{",".join(dropdown_values)}"'
    # 创建一个数据验证对象，指定下拉框选项
    dv = DataValidation(type="list", formula1=f, )

    for row in range(2, len(dropdown_values) + 10):
        dv.add(sheet[f'A{row}'])  # 应用到第一列（除标题行外）

    # 将数据验证对象添加到工作表中
    sheet.add_data_validation(dv)

    # 保存工作簿
    wb.save(save_path)


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
    columns2 = ["映射名称", "商品编码"]
    df = pd.DataFrame(columns=columns2)
    df.to_excel(writer, index=False, sheet_name="推广模板", )

    # 生成商品模板
    stract_list = CodeStractModel.query.all()
    column = ["标题", "SKU名称", "店铺", "商品名称", '商品编码', "原材料", "成本明细", "创建时间", ]
    stract_info = []
    for stract in stract_list:
        if stract.sale:
            sale = stract.sale
            for atom in sale.atoms:
                cost = atom.cost
                atom_name = atom.name
                title = stract.store_title
                name = stract.name
                store = stract.store.name if stract.store else ""
                sale_name = stract.sale.name if stract.sale else ""
                sale_code = stract.sale.code if stract.sale else ""

                create_time = stract.createTime.strftime("%Y-%m-%d %H:%M:%S")
                sale_list = [title, name, store, sale_name, sale_code, atom_name, cost, create_time]
                stract_info.append(sale_list)
        else:
            title = stract.store_title
            name = stract.name
            store = stract.store.name if stract.store else ""
            sale_name = stract.sale.name if stract.sale else ""
            sale_code = stract.sale.code if stract.sale else ""

            create_time = stract.createTime.strftime("%Y-%m-%d %H:%M:%S")
            sale_list = [title, name, store, sale_name, sale_code, "未绑定映射", "未绑定映射成本", create_time]

            stract_info.append(sale_list)
    df = pd.DataFrame(stract_info, columns=column)
    df.to_excel(writer, index=False, sheet_name="商品模板")

    writer.close()
