from APP.SQLAPP.addEdit.dataWrite import dealDate
from APP.SQLAPP.addEdit.orderStore import writeStore, writeAdMethodModel, writeNewDisModel
from APP.SQLAPP.search.product import refreshSaleFile

from APP.Spyder.KdzsSpyder import KuaiDiZhuShouSpyder
from form.formValidate import KdzsLoginForm, DisForm, newStoreProForm, OrderForm
from flask import Blueprint, request, current_app, render_template, send_file, \
    jsonify

from models.back import PlatModel, CityModel, AdMethodModel
from models.store import StoreModel, DistributionModel

bp = Blueprint("store", __name__, url_prefix="/store")
kdzs = KuaiDiZhuShouSpyder()


@bp.route("/manage")
def manage():
    plats = PlatModel.query.all()
    citys = CityModel.query.all()
    stores = StoreModel.query.all()
    adMethods = AdMethodModel.query.all()
    distributions = DistributionModel.query.all()
    return render_template("html/back/storeManage.html", stores=stores, plats=plats, citys=citys, adMethods=adMethods,
                           distributions=distributions)


@bp.route("/loginKdzs", methods=['POST'])
def loginKdzs():
    form_dict = request.form.to_dict()
    form = KdzsLoginForm(form_dict)
    if form.validate():
        result = kdzs.login(account=form_dict.get("kdzsAccount"), password=form_dict.get("kdzsPassword"),
                            captcha=form_dict.get("kdzsCaptcha"),vscode=form_dict.get("kdzsPhoneCode"))
        if result.get("status") == "success":
            return jsonify({"status": "success", "message": "登录成功"})
        else:
            return jsonify({"status": "failed", "message": result.get("message")})
    else:
        return jsonify({"status": "failed", "message": form.messages})


# 获取图片验证码
@bp.route("/kdzsCaptcha")
def kdzsCaptcha():
    testResult = kdzs.getCaptcha()
    print(testResult)
    return jsonify(testResult)


@bp.route("/kdzsTest")
def kdzsTest():
    testResult = kdzs.TestCookie()
    return jsonify(testResult)


@bp.route("/kdzsStore")
def kdzsStore():
    StoreResult = kdzs.gerStoreKDZS()
    if StoreResult['status'] == "success":
        store_list = StoreResult['data']
        new_store = writeStore(store_list)
        if len(new_store) > 0:
            return jsonify({"status": "success", "message": "更新完成"})
        else:
            return jsonify({"status": "failed", "message": "没有发现新店铺"})
    else:
        return jsonify({"status": "failed", "message": "获取店铺信息失败"})


@bp.route("/getStoreOrder", methods=['POST'])
def getStoreOrder():
    form_dict = request.form.to_dict()
    print(form_dict)
    form = OrderForm(form_dict)
    if form.validate():
        if form_dict.get("kdzsDayLength"):
            startDate, endDate = dealDate(now=True, length=form_dict.get("kdzsDayLength"))
        else:
            startDate, endDate = dealDate(start_date=form_dict.get("kdzsStartDate"),
                                          end_date=form_dict.get("kdzsEndDate"))
        print(startDate, endDate)
        if startDate < endDate:
            stores = getStore(form_dict.get("kdzsStore"))
            current_app.celery.send_task("GetOrders", (stores, endDate, startDate))
            return jsonify({"status": "success", "message": "已经开始获取订单信息,请稍后查看.."})
        else:
            return jsonify({"status": "failed", "message": "开始时间需要小于结束时间.."})
    else:
        return jsonify({"status": "failed", "message": form.messages})


@bp.route("/getStoreRefund", methods=['POST'])
def getStoreRefund():
    form_dict = request.form.to_dict()
    print(form_dict)
    form = OrderForm(form_dict)
    if form.validate():
        if form_dict.get("kdzsDayLength"):
            startDate, endDate = dealDate(now=True, length=form_dict.get("kdzsDayLength"), zero=True)
        else:
            startDate, endDate = dealDate(start_date=form_dict.get("kdzsStartDate"),
                                          end_date=form_dict.get("kdzsEndDate"), zero=True)
        if startDate < endDate:
            current_app.celery.send_task("GetRefund", (endDate, startDate))
            return jsonify({"status": "success", "message": "已经开始获取订单信息,请稍后查看.."})
        else:
            return jsonify({"status": "failed", "message": "开始时间需要小于结束时间.."})
    else:
        return jsonify({"status": "failed", "message": form.messages})


@bp.route("/newDis", methods=['POST'])
def newDis():
    form_dict = request.form.to_dict()
    print(form_dict)
    form = DisForm(form_dict)
    if form.validate():
        return writeNewDisModel(form_dict)
    else:
        return jsonify({"status": "failed", "message": form.messages})


@bp.route("/newStorePro", methods=['POST'])
def newStorePro():
    form_dict = request.form.to_dict()
    print(form_dict)
    form = newStoreProForm(form_dict)
    if form.validate():
        return writeAdMethodModel(form_dict)
    else:
        return jsonify({"status": "failed", "message": form.messages})


def getStore(store_id):
    if store_id == "All":
        stores_info = StoreModel.query.filter().all()
    else:
        stores_info = StoreModel.query.filter(StoreModel.id == store_id).all()
    stores = [{"platform": store.plat.EH_name.lower(), "sellerId": store.store_id} for store in stores_info if
              store.plat.EH_name]
    stores.append({"platform": "hand", "sellerId": "1251533"})
    return stores


@bp.route("/refreshSale")
def refreshSale():
    save_path = 'static/excel/sale.xlsx'
    refreshSaleFile()
    return send_file(save_path, as_attachment=True)
