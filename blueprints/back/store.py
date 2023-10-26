from APP.SQLAPP.addEdit.dataWrite import dealDate
from APP.SQLAPP.addEdit.orderStore import writeStore, writeAdMethodModel, writeNewDisModel
from APP.SQLAPP.search.product import refreshSaleFile

from APP.Spyder.KdzsSpyder import KuaiDiZhuShouSpyder
from exts import db
from form.formValidate import KdzsLoginForm, DisForm, newStoreProForm, OrderForm
from flask import Blueprint, request, current_app, render_template, send_file, \
    jsonify

from models.back import PlatModel, CityModel, AdMethodModel
from models.store import StoreModel, DistributionModel, kdzsTokenModel

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


# 获取图片验证码
@bp.route("/kdzsCaptcha")
def kdzsCaptcha():
    testResult = kdzs.getCaptcha()
    return jsonify(testResult)


# 获取token，并且和账号一起写入到数据库中。
@bp.route("/loginKdzs", methods=['POST'])
def loginKdzs():
    form_dict = request.form.to_dict()
    form = KdzsLoginForm(form_dict)
    if form.validate():
        result = kdzs.login(account=form_dict.get("kdzsAccount"), password=form_dict.get("kdzsPassword"),
                            captcha=form_dict.get("kdzsCaptcha"), vscode=form_dict.get("kdzsPhoneCode"))
        if result.get("status") == "success":
            kdzstoken_model = kdzsTokenModel.query.filter_by(name="token").first()
            if not kdzstoken_model:
                kdzstoken_model = kdzsTokenModel(name="token", token=result.get("message"))
            else:
                kdzstoken_model.token = result.get("message")
            db.session.add(kdzstoken_model)
            db.session.commit()
            return jsonify({"status": "success", "message": "登录成功"})
        else:
            return jsonify({"status": "failed", "message": result.get("message")})
    else:
        return jsonify({"status": "failed", "message": form.messages})


@bp.route("/kdzsTest")
def kdzsTest():
    token_model = kdzsTokenModel.query.filter_by(name="token").first()
    if token_model:
        token = token_model.token
        testResult = kdzs.TestCookie(token=token)
        return jsonify(testResult)
    else:
        return {"status": "false", "message": "验证失败，请重新登陆"}


@bp.route("/kdzsStore")
def kdzsStore():
    token_model = kdzsTokenModel.query.filter_by(name="token").first()
    if token_model:
        token = token_model.token
        testResult = kdzs.TestCookie(token=token)
        if testResult.get("status") == "success":
            StoreResult = kdzs.gerStoreKDZS(token=token)
            if StoreResult['status'] == "success":
                store_list = StoreResult['data']
                new_store = writeStore(store_list)
                if len(new_store) > 0:
                    return jsonify({"status": "success", "message": "更新完成"})
                else:
                    return jsonify({"status": "failed", "message": "没有发现新店铺"})
            else:
                return jsonify({"status": "failed", "message": "获取店铺信息失败"})
        else:
            return jsonify(testResult)
    else:
        return {"status": "false", "message": "快递助手令牌已过期,请重新登陆"}


@bp.route("/getStoreOrder", methods=['POST'])
def getStoreOrder():
    token_model = kdzsTokenModel.query.filter_by(name="token").first()
    if token_model:
        token = token_model.token
        testResult = kdzs.TestCookie(token=token)
        if testResult.get("status") == "success":
            form_dict = request.form.to_dict()
            form = OrderForm(form_dict)
            if form.validate():
                if form_dict.get("kdzsDayLength"):
                    startDate, endDate = dealDate(now=True, length=form_dict.get("kdzsDayLength"))
                else:
                    startDate, endDate = dealDate(start_date=form_dict.get("kdzsStartDate"),
                                                  end_date=form_dict.get("kdzsEndDate"))
                if startDate < endDate:
                    stores = getStore(form_dict.get("kdzsStore"))
                    current_app.celery.send_task("GetOrders", (stores, endDate, startDate, token))
                    return jsonify({"status": "success", "message": "已经开始获取订单信息,请稍后查看.."})
                else:
                    return jsonify({"status": "failed", "message": "开始时间需要小于结束时间.."})
            else:
                return jsonify({"status": "failed", "message": form.messages})
        else:
            return jsonify(testResult)
    else:
        return {"status": "false", "message": "快递助手令牌已过期,请重新登陆"}


@bp.route("/getStoreRefund", methods=['POST'])
def getStoreRefund():
    token_model = kdzsTokenModel.query.filter_by(name="token").first()
    if token_model:
        token = token_model.token
        testResult = kdzs.TestCookie(token=token)
        if testResult.get("status") == "success":
            form_dict = request.form.to_dict()
            form = OrderForm(form_dict)
            if form.validate():
                if form_dict.get("kdzsDayLength"):
                    startDate, endDate = dealDate(now=True, length=form_dict.get("kdzsDayLength"))
                else:
                    startDate, endDate = dealDate(start_date=form_dict.get("kdzsStartDate"),
                                                  end_date=form_dict.get("kdzsEndDate"))
                if startDate < endDate:
                    stores = getStore(form_dict.get("kdzsStore"))
                    current_app.celery.send_task("GetRefund", (stores, endDate, startDate, token))
                    return jsonify({"status": "success", "message": "已经开始获取订单信息,请稍后查看.."})
                else:
                    return jsonify({"status": "failed", "message": "开始时间需要小于结束时间.."})
            else:
                return jsonify({"status": "failed", "message": form.messages})
        else:
            return jsonify(testResult)
    else:
        return {"status": "false", "message": "快递助手令牌已过期,请重新登陆"}


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
    stores = []
    if store_id == "All":
        stores_info = StoreModel.query.filter().all()
    else:
        stores_info = [StoreModel.query.get(store_id)]
    for store in stores_info:
        if store.name == "手工单":
            pass
        elif store.plat.EH_name:
            stores.append({"platform": store.plat.EH_name.lower(), "sellerId": store.store_id})
    stores.append({"platform": "hand", "sellerId": "1251533"})
    return stores


@bp.route("/refreshSale")
def refreshSale():
    save_path = 'static/excel/sale.xlsx'
    refreshSaleFile()
    return send_file(save_path, as_attachment=True)
