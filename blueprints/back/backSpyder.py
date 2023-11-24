import os
import re

from APP.SQLAPP.addEdit.orderStore import WriteExcelOrder
from APP.SQLAPP.addEdit.promotion import WriteSQLData
from APP.SQLAPP.changeSql.changeSQL import ChangeSQL
from APP.SQLAPP.search.promotion import dyToken, xhsToken, searchPVContentSql, searchPVContentSql2, searchNotes
from APP.Spyder.DySpyder import DouYinSpyder
from APP.Spyder.KsSpyder import KuaiShouSpyder
from APP.Spyder.XshSpyder import GetXhsSpyder
from APP.SQLAPP.addEdit.dataWrite import writeSimpleModelData, writeNewPromotionPlatModel, writeXhsTokenModel
from APP.Spyder.makeRealURL import MakeRealURL
from exts import db

from form.formValidate import KsLoginForm, \
    XhsForm, DyForm
from flask import Blueprint, request, render_template, jsonify, current_app, url_for, redirect

from models.back import UnitModel, AtomCategoryModel, BrandModel, OutputModel, FeeModel, PlatModel, RateModel, \
    CityModel, XhsTokenModel, DyTokenModel
from models.promotion import AccountModel
from models.promotiondata import PVContentModel
from models.store import HandOrderCategory

bp = Blueprint("spyder", __name__, url_prefix="/spyder")
ks = KuaiShouSpyder()
xhs = GetXhsSpyder()
dy = DouYinSpyder()
makeRealURL = MakeRealURL()


@bp.route("/manage")
def manage():
    content_plats = PVContentModel.query.filter().join(PVContentModel.account).join(AccountModel.plat).with_entities(
        PlatModel.name).distinct().all()
    attentions = PVContentModel.query.with_entities(PVContentModel.attention.label("attention")).distinct().all()
    xhs_tokens = XhsTokenModel.query.all()
    dy_tokens = DyTokenModel.query.all()
    return render_template("html/back/spyderManage.html", xhs_tokens=xhs_tokens, content_plats=content_plats,
                           dy_tokens=dy_tokens,
                           attentions=attentions)


@bp.route("/loginKs", methods=['POST'])
def loginKs():
    form_dict = request.form.to_dict()
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
        return redirect(url_for("spyder.manage"))
    else:
        return redirect(url_for("spyder.manage"))


@bp.route("/editdyToken", methods=['POST'])
def editdyToken():
    form_dict = request.form.to_dict()
    form = DyForm(form_dict)
    if form.validate():
        id = form_dict.get("token_id")
        token = form_dict.get("xhsToken")
        model = DyTokenModel.query.filter_by(id=id).first()
        model.name = token
        db.session.commit()
        return redirect(url_for("spyder.manage"))
    else:
        return redirect(url_for("spyder.manage"))


@bp.route("/testXhs")
def testXhs():
    token_id = request.args.get("token_id")
    if token_id:
        token_model = XhsTokenModel.query.filter_by(id=token_id).first()
        test_result = xhs.testCookie(token=token_model.name)
        if test_result['message'] == "Spam":
            token_model.status = "触发反爬"
            db.session.commit()
            return jsonify({"message": "触发反爬"})
        elif test_result["message"] == "登录已过期":
            token_model.status = "登录已过期"
            db.session.add(token_model)
            db.session.commit()
            return {"status": "2", "message": "登录已过期，请重新登录"}
        else:
            token_model.status = "正常"
            db.session.commit()
            return jsonify({"message": "正常"})
    else:
        token_list = db.session.query(XhsTokenModel.name).all()
        message = ""
        for token in token_list:
            token_model = XhsTokenModel.query.filter_by(name=token[0]).first()
            test_result = xhs.testCookie(token=token[0])
            if test_result['message'] == "Spam":
                token_model.status = "触发反爬"
                message += token[0] + "触发反爬"
            elif test_result["message"] == "登录已过期":
                token_model.status = "登录已过期"
                message += token[0] + "登录已过期"

            else:
                token_model.status = "正常"
                message += token[0] + "正常"
            db.session.commit()
        return jsonify({"message": message})


@bp.route("/loginDy", methods=['POST'])
def loginDy():
    form_dict = request.form.to_dict()
    form = DyForm(form_dict)
    if form.validate():
        name = form_dict.get("name")
        wechat = form_dict.get("dyName")
        phone = form_dict.get("dyPhone")
        return writeXhsTokenModel(Model=DyTokenModel, name=name, wechat=wechat, phone=phone)
    else:
        return jsonify({"status": "failed", "message": form.messages})


@bp.route("/testDy")
def testDy():
    token_id = request.args.get("token_id")
    if token_id:
        token_model = DyTokenModel.query.filter_by(id=token_id).first()
        test_result = dy.testCookie(token=token_model.name)
        if test_result['message'] == "登录已过期":
            token_model.status = "登录已过期"
            db.session.add(token_model)
            db.session.commit()
            return {"status": "2", "message": "登录已过期，请重新登录"}
        else:
            token_model.status = "正常"
            db.session.commit()
            return jsonify({"message": "正常"})
    else:
        token_list = db.session.query(DyTokenModel.name, DyTokenModel.phone).all()
        message = ""
        for token in token_list:
            token_model = DyTokenModel.query.filter_by(name=token.name).first()
            test_result = dy.testCookie(token=token[0])
            if test_result["message"] == "登录已过期":
                token_model.status = "登录已过期"
                message += token.phone + " 登录已过期"
            else:
                token_model.status = " 正常"
                message += token.phone + " 正常"
            db.session.commit()
            print(message)
        return jsonify({"message": message})


@bp.route("/getPVcontentData")
def getPVcontentData():
    plat = request.args.get("plat")
    attention = request.args.get("attention")
    print(plat, attention)
    plat = "" if plat == "null" else plat
    attention = "" if attention == "null" else attention
    if plat:
        result = sypderCelery(plat=plat, attention=attention)
        if not result:
            return jsonify({"status": "failed", "message": "暂不支持该平台的内容爬取"})
        else:
            return jsonify({"status": "success", "message": "正在更新内容数据"})
    else:
        return jsonify({"status": "failed", "message": "请选择平台"})


def sypderCelery(plat, attention):
    if plat == "小红书":
        current_app.celery.send_task("GetXHSNote", (attention, plat,))
        return True
    elif plat == "抖音":
        current_app.celery.send_task("GetDYNote", (attention, plat,))
        return True
    elif plat == "快手":
        current_app.celery.send_task("GetKSNote", (attention, plat,))
        return True
    else:
        return False


@bp.route("/addAccount", methods=['POST'])
def addAccount():
    account_link = request.form.to_dict().get("newXHSAccount")
    note_info = request.form.to_dict().get("note_info")
    # ChangeSQL().changeAccountLink()
    # return jsonify({"status": "success", "message": "新增抖音账号成功"})
    # print(account_link, note_info)
    if "www.xiaohongshu.com" in account_link:
        token = xhsToken()
        xhs = GetXhsSpyder()
        base_url = "https://www.xiaohongshu.com/user/profile/"
        if "profile" and "user" in account_link:
            account_link = account_link.split("?")[0] if "?" in account_link else account_link
            uid = re.findall(r"profile/(.+)", account_link)[0]
            profile_link = base_url + uid
            result = xhs.getUserInfo(token=token, url=profile_link)
            if result["status"] == "1":
                write = WriteSQLData()
                account_Info = result["message"]
                selfs = "自营"
                write.WriteSqlAccount(profile_link=profile_link, account_Info=account_Info, plat="小红书", selfs=selfs)
                notes = int(account_Info.get("notes")) if account_Info.get("notes") else 0
                if notes > 0 and note_info == "1":
                    current_app.celery.send_task("GetXHSAccountNote", (profile_link, notes,))
                return jsonify({"status": "success", "message": f"新增小红书账号{account_Info.get('nickname')}成功"})
            else:
                return jsonify({"status": "failed", "message": result["message"]})
        else:
            return jsonify({"status": "failed", "message": "请输入正确的小红书主页链接"})

    elif "www.douyin.com" in account_link:
        print("抖音")
        return jsonify({"status": "failed", "message": "新增抖音账号成功"})
    else:
        return jsonify({"status": "failed", "message": "请输入正确的主页链接"})
