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
