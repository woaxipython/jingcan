import os

from APP.SQLAPP.addEdit.orderStore import WriteExcelOrder
from APP.SQLAPP.search.promotion import dyToken, xhsToken
from APP.Spyder.DySpyder import DouYinSpyder
from APP.Spyder.KsSpyder import KuaiShouSpyder
from APP.Spyder.XshSpyder import GetXhsSpyder
from APP.SQLAPP.addEdit.dataWrite import writeSimpleModelData, writeNewPromotionPlatModel, writeXhsTokenModel
from blueprints.handOrderManage import handOrderName
from blueprints.sale.saleManage import allExcelFile
from exts import db
from form.fileValidate import HandOrderFile

from form.formValidate import KsLoginForm, \
    XhsForm, DyForm
from flask import Blueprint, request, render_template, jsonify, current_app, url_for, redirect

from models.back import UnitModel, AtomCategoryModel, BrandModel, OutputModel, FeeModel, PlatModel, RateModel, \
    CityModel, XhsTokenModel, DyTokenModel
from models.store import HandOrderCategory

bp = Blueprint("back", __name__, url_prefix="/back")
ks = KuaiShouSpyder()
xhs = GetXhsSpyder()
dy = DouYinSpyder()


@bp.route("/basicSelect")
def basicSelect():
    units = UnitModel.query.all()
    atom_categories = AtomCategoryModel.query.all()
    brands = BrandModel.query.all()
    outputs = OutputModel.query.all()
    feeModels = FeeModel.query.all()
    plats = PlatModel.query.all()
    rates = RateModel.query.all()
    handsTypes = HandOrderCategory.query.all()

    return render_template("html/back/basicSelect.html", units=units, atom_categories=atom_categories, brands=brands,
                           outputs=outputs, feeModels=feeModels, plats=plats, rates=rates, handsTypes=handsTypes,
                           )


@bp.route("/spyderManage")
def spyderManage():
    xhs_tokens = XhsTokenModel.query.all()
    return render_template("html/back/spyderManage.html", xhs_tokens=xhs_tokens)


@bp.route("/loginKs", methods=['POST'])
def loginKs():
    form_dict = request.form.to_dict()
    print(form_dict)
    form = KsLoginForm(form_dict)
    if form.validate():
        result = ks.login(phone=form_dict.get("ksAccount"), smsCode=form_dict.get("ksPhoneCode"))
        return jsonify(result)
    else:
        return jsonify({"status": "failed", "message": form.messages})


@bp.route("/getPhoneCodeKs")
def getPhoneCodeKs():
    result = ks.getMobileCode()
    return jsonify(result)


@bp.route("/testKs")
def testKs():
    testResult = ks.TestCookie()
    return jsonify(testResult)


@bp.route("/loginXhs", methods=['POST'])
def loginXhs():
    form_dict = request.form.to_dict()
    form = XhsForm(form_dict)
    if form.validate():
        name = form_dict.get("xhsToken")
        wechat = form_dict.get("xhsWechat")
        phone = form_dict.get("xhsPhone")
        return writeXhsTokenModel(Model=XhsTokenModel, name=name, wechat=wechat, phone=phone)
    else:
        return jsonify({"status": "failed", "message": form.messages})


@bp.route("/editXhsToken", methods=['POST'])
def editXhsToken():
    form_dict = request.form.to_dict()
    form = XhsForm(form_dict)
    if form.validate():
        id = form_dict.get("token_id")
        token = form_dict.get("xhsToken")
        model = XhsTokenModel.query.filter_by(id=id).first()
        model.name = token
        db.session.commit()
        return redirect(url_for("back.spyderManage"))
    else:
        return redirect(url_for("back.spyderManage"))


@bp.route("/testXhs")
def testXhs():
    token_id = request.args.get("token_id")
    if token_id:
        token = XhsTokenModel.query.filter_by(id=token_id).first()
        testResult = xhs.testCookie(token=token.name)
        if testResult['message'] == "Spam":
            token.status = "触发反爬"
            db.session.commit()
            return jsonify({"message": "触发反爬"})
        else:
            token.status = "正常"
            db.session.commit()
            return jsonify({"message": "正常"})
    else:
        token_list = db.session.query(XhsTokenModel.name).all()
        print(token_list)
        message = ""
        for token in token_list:
            token_model = XhsTokenModel.query.filter_by(name=token[0]).first()
            test_result = xhs.testCookie(token=token[0])
            if test_result['message'] == "Spam":
                token_model.status = "触发反爬"
                db.session.commit()
                message += token[0] + "触发反爬"
            else:
                token_model.status = "正常"
                db.session.commit()
                message += token[0] + "正常"
        return jsonify({"message": message})


@bp.route("/loginDy", methods=['POST'])
def loginDy():
    form_dict = request.form.to_dict()
    print(form_dict)
    print(len(form_dict['name']))
    form = DyForm(form_dict)
    if form.validate():
        name = form_dict.get("name")
        return writeSimpleModelData(Model=DyTokenModel, name=name)
    else:
        return jsonify({"status": "failed", "message": form.messages})


@bp.route("/testDy")
def testDy():
    return jsonify(dy.testCookie(token=dyToken()))


@bp.route("/newUnit", methods=['POST'])
def newUnit():
    form_dict = request.form.to_dict()
    name = form_dict.get("newUnit")
    if 1 <= len(name) < 10:
        return writeSimpleModelData(UnitModel, name)
    else:
        return jsonify({"status": "failed", "message": "名称长度不符合要求，长度在2-10之间"})


@bp.route("/newAtomCategory", methods=['POST'])
def newAtomCategory():
    form_dict = request.form.to_dict()
    name = form_dict.get("newAtomCategory")
    print(form_dict)
    if 2 < len(name) < 10:
        return writeSimpleModelData(AtomCategoryModel, name)
    else:
        return jsonify({"status": "failed", "message": "名称长度不符合要求，长度在2-10之间"})


@bp.route("/newBrand", methods=['POST'])
def newBrand():
    form_dict = request.form.to_dict()
    name = form_dict.get("newBrand")
    print(form_dict)
    if 1 < len(name) < 10:
        return writeSimpleModelData(BrandModel, name)
    else:
        return jsonify({"status": "failed", "message": "名称长度不符合要求，长度在2-10之间"})


@bp.route("/newOutPutModel", methods=['POST'])
def newOutPutModel():
    form_dict = request.form.to_dict()
    print(form_dict)
    name = form_dict.get("newOutPutModel")
    if 1 < len(name) < 10:
        return writeSimpleModelData(OutputModel, name)
    else:
        return jsonify({"status": "failed", "message": "名称长度不符合要求，长度在2-10之间"})


@bp.route("/newFeeModel", methods=['POST'])
def newFeeModel():
    form_dict = request.form.to_dict()
    print(form_dict)
    name = form_dict.get("newFeeModel")
    if 1 < len(name) < 10:
        return writeSimpleModelData(FeeModel, name)
    else:
        return jsonify({"status": "failed", "message": "名称长度不符合要求，长度在2-10之间"})


@bp.route("/newPromotionPlat", methods=['POST'])
def newPromotionPlat():
    form_dict = request.form.to_dict()
    name = form_dict.get("newPromotionPlat")
    print(form_dict)
    if 1 < len(name) < 10:
        return writeNewPromotionPlatModel(Model=PlatModel, name=name)
    else:
        return jsonify({"status": "failed", "message": "名称长度不符合要求，长度在2-10之间"})


@bp.route("/newPromotionRate", methods=['POST'])
def newPromotionRate():
    form_dict = request.form.to_dict()
    print(form_dict)
    name = form_dict.get("newPromotionRate")
    if 1 < len(name) < 10:
        return writeSimpleModelData(RateModel, name)
    else:
        return jsonify({"status": "failed", "message": "名称长度不符合要求，长度在2-10之间"})


@bp.route("/newHandOrderType", methods=['POST'])
def newHandOrderType():
    form_dict = request.form.to_dict()
    print(form_dict)
    name = form_dict.get("newHandOrderType")
    if 1 < len(name) < 10:
        return writeSimpleModelData(HandOrderCategory, name)
    else:
        return jsonify({"status": "failed", "message": "名称长度不符合要求，长度在2-10之间"})


@bp.route("/refreshLocation")
def refreshLocation():
    current_app.celery.send_task("GetAddress")
    return jsonify({"status": "failed", "message": "正在刷新地区数据..."})


@bp.route("/getCityArea")
def getCityArea():
    city = request.args.get("city")
    sql_areas = CityModel.query.filter_by(name=city).first().provinces
    areas = [
        {"name": area.name} for area in sql_areas
    ]
    return jsonify({"status": "failed", "message": areas})


@bp.route("/handOrder")
def handOrder():
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
                    return jsonify(write.writeHandOrder())
                else:
                    return jsonify(make_result)
            else:
                return jsonify({"status": "failed", "message": "请选择正确的分销商或发货人"})
        else:
            return jsonify({'status': 'failed', 'message': form.messages})
    else:
        return jsonify({"status": "failed", "message": "请上传正确的文件"})
