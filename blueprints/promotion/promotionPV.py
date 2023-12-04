import os
from datetime import datetime

from APP.SQLAPP.addEdit.promotion import writeNewPromotionModel, writePromotionFee
from APP.SQLAPP.makePandas.promotion import makePVEcel
from APP.SQLAPP.search.promotion import searchAccount, searchPVContentSql, searchNotes
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
    pvcontent = PVContentModel.query.filter(PVContentModel.id == search_id).first()
    pvcontent.attention = 1 if attention == "1" else 0
    db.session.commit()

    attention_status = PVContentModel.query.filter(PVContentModel.id == search_id).first().attention
    message = "取消关注" if attention_status == 1 else "关注"
    return jsonify({"status": "success", "message": message})


@bp.route("/downloadpv", methods=['GET', 'POST'])
def downloadpv():
    plat = request.args.get("plat")
    if plat == "dy":
        plat = "抖音"
    elif plat == "xhs":
        plat = "小红书"
    else:
        plat = "其他"
    pvcontents = searchPVContentSql(plat=plat)
    save_path = 'static/excel/推广数据下载.xlsx'.format(plat)
    makePVEcel(pvcontents, save_path)
    return send_file(save_path, as_attachment=True)


def dataManage(plat):
    plats = PlatModel.query.all()
    accounts = AccountModel.query.with_entities(AccountModel.id, AccountModel.nickname, AccountModel.self).filter(
        AccountModel.self == "自营", AccountModel.nickname != None,  AccountModel.nickname != "",PlatModel.name == plat).join(
        AccountModel.plat).distinct().all()
    selfs = AccountModel.query.with_entities(AccountModel.self.label("name")).distinct().all()
    contenttypes = PVContentModel.query.with_entities(PVContentModel.contenttype.label("name")).distinct().all()
    groups = GroupModel.query.all()

    end_date = datetime.now().strftime("%Y-%m-%d")
    if plat == "抖音":
        title = "抖音图文管理"
        title_id = "dy"
    elif plat == "小红书":
        title = "小红书图文管理"
        title_id = "xhs"
    else:
        title = "图文管理"
        title_id = "other"
    if request.method == "POST":
        interval = convert_to_number(request.form.get("interval"))
        self = request.form.get("self")
        liked_s, liked_e = split_num(request.form.get("liked"))
        commented_s, commented_e = split_num(request.form.get("commented"))
        collected_s, collected_e = split_num(request.form.get("collected"))

        contenttype = request.form.get("contenttype")
        nickname = request.form.get("nickname")
        group = request.form.get("group_name")
        pvcontents = searchPVContentSql(end_date=end_date, interval=interval, plat=plat, group=group, self=self,
                                        liked_s=liked_s, liked_e=liked_e, commented_s=commented_s, nickname=nickname,
                                        commented_e=commented_e, collected_s=collected_s, collected_e=collected_e,
                                        contenttype=contenttype)
    else:
        pvcontents = searchPVContentSql(end_date=end_date, plat=plat)
    return render_template("html/promotion/promotionPV.html", selfs=selfs, accounts=accounts, plats=plats,
                           groups=groups, contenttypes=contenttypes, title=title, pvcontents=pvcontents,
                           title_id=title_id)

def split_num(num):
    if num:
        num_list = num.split(",")
        return int(num_list[0]), int(num_list[1])
    else:
        return ("-1", "2000000000")
