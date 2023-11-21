import os
from datetime import datetime

from APP.SQLAPP.addEdit.promotion import writeNewPromotionModel, writePromotionFee
from APP.SQLAPP.makePandas.promotion import PromotionData
from APP.SQLAPP.search.promotion import searchAccount, searchPVContentSql, searchNotes, makePromotionExcel, \
    GetPromotionModel
from blueprints.sale.saleManage import allExcelFile, convert_to_number
from exts import db
from form.fileValidate import PromotionFileForm

from form.formValidate import NewPromotionForm, EditPromotionForm, ProfileLinkForm, NotesLinkForm, GetPromotionForm
from flask import Blueprint, request, current_app, render_template, send_file, \
    jsonify, redirect, url_for

from models.back import PlatModel, RateModel, FeeModel, OutputModel
from models.product import GroupModel
from models.promotion import PromotionModel, AccountModel
from models.promotiondata import PVContentModel
from models.user import UserModel

bp = Blueprint("pv", __name__, url_prefix="/pv")


@bp.route("/xhsmanage", methods=['GET', 'POST'])
def xhsmanage():
    return dataManage("小红书")


@bp.route("/dymanage", methods=['GET', 'POST'])
def dymanage():
    return dataManage("抖音")


@bp.route("/attention")
def attention():
    search_id = request.args.get("search_id")
    attention = request.args.get("attention")
    print(search_id)
    print(attention)
    pvcontent = PVContentModel.query.filter(PVContentModel.search_id == search_id).first()
    pvcontent.attention = 1 if attention == "1" else 0
    db.session.commit()
    message = "取消关注" if attention == "1" else "关注"
    print(message)
    return jsonify({"status": "success", "message": message})


def dataManage(plat):
    plats = PlatModel.query.all()
    accounts = AccountModel.query.with_entities(AccountModel.id, AccountModel.nickname, AccountModel.self).filter(
        AccountModel.self == True).all()
    selfs = AccountModel.query.with_entities(AccountModel.self.label("name")).distinct().all()
    contenttypes = PVContentModel.query.with_entities(PVContentModel.contenttype.label("name")).distinct().all()
    groups = GroupModel.query.all()
    users = db.session.query(UserModel.id, UserModel.name).all()
    rates = RateModel.query.all()
    fee_models = FeeModel.query.all()
    outputs = OutputModel.query.all()
    end_date = datetime.now().strftime("%Y-%m-%d")
    pvcontents = searchPVContentSql(end_date=end_date, plat=plat)
    if plat == "抖音":
        title = "抖音图文管理"
    elif plat == "小红书":
        title = "小红书图文管理"
    else:
        title = "图文管理"
    if request.method == "POST":
        interval = convert_to_number(request.form.get("interval"))
        self = request.form.get("self")
        contenttype = request.form.get("contenttype")
        nickname = request.form.get("nickname")
        group = request.form.get("group_name")

        pvcontents = searchPVContentSql(end_date=end_date, interval=interval, plat="抖音", group=group, )
    return render_template("html/promotion/promotionPV.html", selfs=selfs, accounts=accounts, plats=plats,
                           groups=groups, contenttypes=contenttypes, title=title,
                           users=users, rates=rates,
                           feeModels=fee_models, outputs=outputs, pvcontents=pvcontents)
