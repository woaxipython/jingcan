from datetime import datetime

from APP.SQLAPP.addEdit.promotion import writeNewPromotionModel, writePromotionFee
from APP.SQLAPP.search.promotion import searchAccount, searchPVContentSql, searchNotes, searchAccountSql, \
    searchAccountSql3
from blueprints.promotion.promotionPV import split_num
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

bp = Blueprint("outAccount", __name__, url_prefix="/outAccount")


@bp.route("/manage", methods=['GET', 'POST'])
def manage():
    plats = AccountModel.query.with_entities(PlatModel.id, PlatModel.name).filter(
        AccountModel.self == "自营", AccountModel.nickname != None).join(AccountModel.plat).distinct().all()
    nicknames = AccountModel.query.with_entities(AccountModel.id, AccountModel.nickname, AccountModel.self).filter(
        AccountModel.self == "自营", AccountModel.nickname != None).distinct().all()
    selfs = AccountModel.query.with_entities(AccountModel.self.label("name")).distinct().all()

    title = "账号管理"
    title_id = "account"
    if request.method == "POST":
        plat = request.form.get("plat")
        nickname = request.form.get("nickname")
        accounts = searchAccountSql(plat=plat, nickname=nickname)
    else:
        accounts = searchAccountSql()
    return render_template("html/promotion/outAccount.html", selfs=selfs, nicknames=nicknames, plats=plats, title=title,
                           accounts=accounts,
                           title_id=title_id)


@bp.route("/attention", methods=['GET', 'POST'])
def attention():
    account_id = request.args.get("account_id")
    attention = request.args.get("attention")
    print(account_id, attention)
    account = AccountModel.query.filter(AccountModel.account_id == account_id).first()
    account.attention = 1 if attention == "1" else 0
    db.session.commit()

    attention_status = AccountModel.query.filter(AccountModel.account_id == account_id).first().attention
    message = "取消关注" if attention_status == 1 else "关注"
    return jsonify({"status": "success", "message": message})


@bp.route("/Notes", methods=['GET', 'POST'])
def Notes():
    account_id = request.args.get("account_id")
    pvcontents = searchAccountSql3(account_id=account_id)
    plats = PlatModel.query.all()
    account = AccountModel.query.filter(AccountModel.account_id == account_id).first()
    accounts = AccountModel.query.with_entities(AccountModel.id, AccountModel.nickname, AccountModel.self).filter(
        AccountModel.self == "自营", AccountModel.nickname != None, AccountModel.nickname != "", ).join(
        AccountModel.plat).distinct().all()
    selfs = AccountModel.query.with_entities(AccountModel.self.label("name")).distinct().all()
    contenttypes = PVContentModel.query.with_entities(PVContentModel.contenttype.label("name")).distinct().all()
    groups = GroupModel.query.all()
    return render_template("html/promotion/promotionPV.html", selfs=selfs, accounts=accounts, plats=plats,
                           groups=groups, contenttypes=contenttypes, title="{} 图文展示".format(account.nickname),
                           pvcontents=pvcontents,
                           title_id=account.account_id)
