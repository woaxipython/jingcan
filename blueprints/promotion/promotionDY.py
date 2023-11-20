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

bp = Blueprint("dy", __name__, url_prefix="/dy")


@bp.route("/manage", methods=['GET', 'POST'])
def manage():
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
    pvcontents = searchPVContentSql(end_date=end_date, plat="抖音")
    if request.method == "POST":
        interval = convert_to_number(request.form.get("interval"))
        self = request.form.get("self")
        contenttype = request.form.get("contenttype")
        nickname = request.form.get("nickname")
        group = request.form.get("group_name")
        print(interval, self, contenttype, nickname, group)

        pvcontents = searchPVContentSql(end_date=end_date, interval=interval, plat="抖音", group=group, )
    return render_template("html/promotion/promotionDY.html", selfs=selfs, accounts=accounts, plats=plats,
                           groups=groups, contenttypes=contenttypes,
                           users=users, rates=rates,
                           feeModels=fee_models, outputs=outputs, pvcontents=pvcontents)


@bp.route("/downFile")
def downFile():
    save_path = 'static/excel/推广批量上传模板.xlsx'
    makePromotionExcel(save_path)
    return send_file(save_path, as_attachment=True)


@bp.route("/FilePromotion", methods=['POST'])
def FilePromotion():
    file = request.files.get("file")
    if file and allExcelFile(file.filename):
        filename = "promotion_.xlsx"
        save_path = os.path.join(current_app.config['UPLOADED_FILES_DEST'], filename)
        file.save(save_path)
        form = PromotionFileForm(save_path)
        if form.validate():
            current_app.celery.send_task("writeFilePromotionC", (save_path,))
            return jsonify({"status": "success", "message": "正在上传文件，是否出错请查看日志"})
        else:
            return jsonify({'status': 'failed', 'message': form.messages})
    else:
        return jsonify({"status": "failed", "message": "请上传正确的文件"})


@bp.route("/data")
def data():
    promotions = GetPromotionModel(interval=9000)
    promotions = promotions.getSQlData()
    promotions = PromotionData(promotions)
    return jsonify({"status": "success", "message": promotions})


@bp.route("/new", methods=['POST'])
def newPromotion():
    """新建推广"""
    form_dict = request.get_json() or request.form.to_dict() or request.args.to_dict()  # 优先级 json > form > args 获取数据
    form = NewPromotionForm(form_dict)  # 验证数据
    if form.validate():
        write = writeNewPromotionModel(form_dict)  # 写入数据
        if write.check():
            return jsonify(write.write())
        else:
            return jsonify({"status": "failed", "message": write.error_message})
    else:
        return jsonify({"status": "failed", "message": form.messages})


@bp.route("/edit", methods=['POST'])
def editPromotion():
    form_dict = request.form.to_dict()
    file = request.files.get("file")
    form = EditPromotionForm(form_dict)
    if form.validate():  # 验证数据
        if file and allowImageFile(file.filename):  # 验证图片
            filename = makeImgaName(form_dict["editPromotionId"], file)  # 生成图片名
            save_path = os.path.join(current_app.config['UPLOADED_IMAGE_DEST'], filename)  # 保存路径
            file.save(save_path)  # 保存图片
        else:
            filename = ""
        write = writePromotionFee(form_dict, save_path=filename)  # 写入数据
        if write.check():
            return jsonify(write.write())
        else:
            return jsonify({"status": "failed", "message": write.error_message})

    else:
        print(form.messages)
        return jsonify({"status": "failed", "message": form.messages})


@bp.route("/getAccount", methods=['POST'])
def getAccount():
    form_dict = request.form.to_dict()
    form = ProfileLinkForm(form_dict)  # 验证数据
    if form.validate():
        write = searchAccount(form_dict)  # 写入数据
        if write.check():
            spyder_result = write.sypderAccount()  # 爬取数据
            if spyder_result["status"] == "success":  # 爬取成功
                return jsonify(write.writeAccount())  # 返回写入数据
            else:  # 爬取失败
                return jsonify(spyder_result)  # 返回爬取失败信息
        else:
            return jsonify({"status": "failed", "message": write.error_message})
    else:
        return jsonify({"status": "failed", "message": form.messages})


@bp.route("/getNotes", methods=['POST'])
def getNotes():
    form_dict = request.form.to_dict()
    form = NotesLinkForm(form_dict)
    if form.validate():
        write = searchNotes(form_dict)
        if write.check():
            spder_result = write.spyderNote()
            if spder_result["status"] == "success":
                return jsonify(write.writeNote())
            else:
                return jsonify(spder_result)
        else:
            return jsonify({"status": "failed", "message": write.error_message})
    else:
        print(form.messages)
        return jsonify({"status": "failed", "message": form.messages})


def allowImageFile(filename):
    return '.' in filename and filename.split('.')[1].lower() in current_app.config.get('IMAGE_ALLOWED_EXTENSIONS')


def makeImgaName(promotionId, file):
    random_name = "".join([str(0) for i in range(0, 10 - len(promotionId))]) + str(promotionId)
    suffix = file.filename.split(".")[1]
    return random_name + "." + suffix
