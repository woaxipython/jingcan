import os

from APP.SQLAPP.addEdit.orderStore import WriteExcelOrder, WriteHandOrder
from APP.SQLAPP.search.orderStore import getHandOrderInfo
from APP.SQLAPP.search.product import downLoadDisFile, makeHandOrderExcel

from blueprints.sale.saleManage import allExcelFile
from form.fileValidate import HandOrderFile
from flask import Blueprint, request, current_app, render_template, send_file, \
    jsonify

from form.formValidate import NewHandOrderForm
from models.back import CityModel
from models.product import SaleModel
from models.store import HandOrderCategory, HandParentOrderModel, DistributionModel
from models.user import UserModel

bp = Blueprint("hand", __name__, url_prefix="/hand")


@bp.route("/order", methods=['GET', 'POST'])
def order():
    sales = SaleModel.query.all()
    users = UserModel.query.all()
    cities = CityModel.query.all()
    handsTypes = HandOrderCategory.query.all()
    diss = DistributionModel.query.all()
    if request.method == "GET":
        handOrders = getHandOrderInfo()
    else:
        form_dict = request.form.to_dict()
        startDate = form_dict.get("startDate")
        endDate = form_dict.get("endDate")
        category = form_dict.get("searchHOCatory")
        status = form_dict.get("searchHOStatus")
        dis = form_dict.get("searchHODis")
        handOrders = getHandOrderInfo(startDate=startDate, endDate=endDate, category=category, status=status, dis=dis)

    return render_template("html/handOrder.html", sales=sales, users=users, cities=cities, handsTypes=handsTypes,
                           diss=diss, handOrders=handOrders)


@bp.route("/new", methods=['POST'])
def newHandOrder():
    form_dict = request.get_json()
    form = NewHandOrderForm(form_dict)
    if form.validate():
        write_hand_order = WriteHandOrder(form_dict)
        if write_hand_order.check():
            if write_hand_order.uploadKdzsOrder():
                return jsonify(write_hand_order.weiteOwnData())
            else:
                return jsonify({"status": "failed", "message": "".join(write_hand_order.error_message)})
        else:
            return jsonify({"status": "failed", "message": "".join(write_hand_order.error_message)})
    else:
        print(form.messages)
        return jsonify({"status": "failed", "message": form.messages})


@bp.route("/disOrder", methods=['POST'])
def newDisOrder():
    form_dict = request.form.to_dict()
    file = request.files.get("file")
    if file and allExcelFile(file.filename):
        filename = handOrderName(filename=file.filename)
        save_path = os.path.join(current_app.config['UPLOADED_FILES_DEST'], filename)
        file.save(save_path)
        form = HandOrderFile(save_path)
        if form.validate():
            write = WriteExcelOrder(form_dict, save_path)
            if write.check():
                make_result = write.makeKdzsExcel()
                if make_result["status"] == "success":
                    upload_result = write.uploadExcelFile()
                    if upload_result["status"] == "success":
                        return jsonify(write.writeHandOrder())
                    else:
                        return jsonify(upload_result)
                else:
                    return jsonify(make_result)
            else:
                return jsonify({"status": "failed", "message": "请选择正确的分销商或发货人"})
        else:
            return jsonify({'status': 'failed', 'message': form.messages})
    else:
        return jsonify({"status": "failed", "message": "请上传正确的文件"})


@bp.route("/downFile")
def downFile():
    save_path = 'static/excel/分销商订单模板.xlsx'
    downLoadDisFile(save_path)
    return send_file(save_path, as_attachment=True)


@bp.route("/downHandOrder", methods=['POST'])
def downHandOrder():
    save_path = 'static/excel/手工订单下载.xlsx'
    form_dict = request.form.to_dict()
    startDate = form_dict.get("startDate")
    endDate = form_dict.get("endDate")
    category = form_dict.get("searchHOCatory")
    status = form_dict.get("searchHOStatus")
    dis = form_dict.get("searchHODis")
    handOrders = getHandOrderInfo(startDate=startDate, endDate=endDate, category=category, status=status, dis=dis)
    makeHandOrderExcel(save_path, handOrders)

    return send_file(save_path, as_attachment=True)


def handOrderName(filename):
    return "handorder." + filename.rsplit('.', 1)[1].lower()
