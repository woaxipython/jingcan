import os
from datetime import datetime

from APP.SQLAPP.addEdit.orderStore import writeStorePromotionFee, WriteStorePromotionFile
from APP.SQLAPP.makePandas.orderStore import makePOrderAll, makePOrderStore, makePOrderMapAll, makePOrderTimeMapAll, \
    makeTimeMapData, makeStoreFeeAllPr
from APP.SQLAPP.search.orderStore import makeStoreProFile, getParentOrders, getParentMap, getParentTimeOrder, \
    getStoreFee
from form.fileValidate import StoreProFile
from form.formValidate import StoreProForm
from flask import Blueprint, request, current_app, render_template, send_file, \
    jsonify
from werkzeug.utils import secure_filename

from models.back import AdMethodModel
from models.product import GroupModel
from models.store import StoreModel

bp = Blueprint("sale", __name__, url_prefix="/sale")


@bp.route("/")
def data():
    stores = StoreModel.query.all()
    adMethods = AdMethodModel.query.all()

    return render_template("html/sale/salesData.html", stores=stores, adMethods=adMethods)


@bp.route("/tmData")
def tmData():
    return render_template("html/sale/tmSalesData.html")


@bp.route("/dyData")
def dyData():
    return render_template("html/sale/dySalesData.html")


@bp.route("/fxData")
def fxData():
    return render_template("html/sale/fxSalesData.html")


@bp.route("/ksData")
def ksData():
    return render_template("html/sale/ksSalesData.html")


@bp.route("/pddData")
def pddData():
    return render_template("html/sale/pddSalesData.html")


@bp.route("/getStoreProFile", methods=['POST'])
def getStoreProFile():
    file = request.files.get('file')
    if file and allExcelFile(file.filename):
        filename = StoreProName(secure_filename(file.filename))
        save_path = os.path.join(current_app.config['UPLOADED_FILES_DEST'], filename)
        file.save(save_path)
        form = StoreProFile(save_path)
        if form.validate():
            writefee = WriteStorePromotionFile(save_path)
            writefee.write()
            if writefee.error_message:
                return jsonify({'status': 'failed', 'message': "".join(writefee.error_message)})
            else:
                return jsonify({"status": "success", 'message': "上传成功"})
        else:
            return jsonify({'status': 'failed', 'message': form.messages})

    return jsonify({"status": "success"})


@bp.route("/getStoreData", methods=['POST'])
def getStoreData():
    form_dict = request.get_json()
    form = StoreProForm(form_dict)
    if form.validate():
        return writeStorePromotionFee(form_dict)
    else:
        return jsonify({'status': 'failed', 'message': form.messages})


@bp.route("/proFileModel")
def proFileModel():
    file_path = "static/excel/推广费模板.xlsx"
    makeStoreProFile(file_path)
    return send_file(file_path, as_attachment=True)


@bp.route("/proinfo")
def proinfo():
    data = []
    store = StoreModel.query.all()
    for i in store:
        store_dict = {
            "storeName": i.name,
            "storeID": i.id,
            'plat': i.plat.name if i.plat else '',
        }
        data.append(store_dict)
    group = GroupModel.query.all()
    group_data = []
    for i in group:
        group_dict = {
            "name": i.name,
            "id": i.id,
        }
        group_data.append(group_dict)
    return jsonify({"status": "success", "data": data, "group": group_data})


@bp.route("/storeData")
def storeData():
    cycle = request.args.get("cycle")
    store = request.args.get("store")
    orders = getParentOrders(status="付款订单", end_date=datetime.now().date().strftime("%Y-%m-%d"),
                             interval=90, store_id="0", count=1)
    totals = makePOrderStore(orders, values="total", cycle=cycle)
    store_total_dict = {
        "date": totals["date"].tolist()
    }
    for column in totals.columns:
        if column != "date":
            store_total_dict[column] = totals[column].tolist()

    counts = makePOrderStore(orders, values="counts", cycle=cycle)

    store_counts_dict = {
        "date": counts["date"].tolist()
    }
    for column in counts.columns:
        if column != "date":
            store_counts_dict[column] = counts[column].tolist()

    return jsonify({"total": store_total_dict, "count": store_counts_dict})


@bp.route("/orderMap")
def orderMap():
    store = request.args.get("store")
    maps = getParentMap(status="付款订单", end_date=datetime.now().date().strftime("%Y-%m-%d"),
                        interval=90, store_id="all", )
    maps_total = makePOrderMapAll(maps, total=True)
    maps_total = round(maps_total, 0)
    maps_total = maps_total.values.tolist()
    return jsonify(maps_total)


@bp.route("/orderTimeMap")
def orderTimeMap():
    store = request.args.get("store")
    time_order = getParentTimeOrder(status="付款订单", end_date=datetime.now().date().strftime("%Y-%m-%d"),
                                    interval=90, store_id="all", )
    time_orders = makePOrderTimeMapAll(time_order)
    time_orders = makeTimeMapData(time_orders)

    return jsonify(time_orders)


@bp.route("/storeAdData")
def storeAdData():
    store = request.args.get("store")
    store_fee = getStoreFee(end_date=datetime.now().date().strftime("%Y-%m-%d"), interval=90, store_id="0", )
    store_fee = makeStoreFeeAllPr(store_fee)
    columns = store_fee.columns.tolist()
    data_dict = {}
    for i in range(len(columns)):
        data_dict[columns[i]] = store_fee.values.T.tolist()[i]
    return jsonify(data_dict)


def allExcelFile(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in current_app.config.get('EXCEL_ALLOWED_EXTENSIONS')


def StoreProName(filename):
    return "handOrder." + filename.rsplit('.', 1)[1].lower()
