import os

from APP.SQLAPP.addEdit.promotion import writePromotionFee
from APP.SQLAPP.makePandas.promotion import promotionChartData
from APP.SQLAPP.search.promotion import searchPVContentSql, makePVContentExcel, searchTotalDataSql
from blueprints.sale.saleManage import allExcelFile
from exts import db
from form.fileValidate import PromotionFileForm

from form.formValidate import NewPromotionForm, EditPromotionForm, ProfileLinkForm, NotesLinkForm, GetPromotionForm
from flask import Blueprint, request, current_app, render_template, send_file, \
    jsonify, redirect, url_for

from models.back import PlatModel, RateModel, FeeModel, OutputModel
from models.product import GroupModel
from models.user import UserModel

bp = Blueprint("promotion", __name__, url_prefix="/promotion")


@bp.route("/manage", methods=['GET', 'POST'])
def manage():
    plats = PlatModel.query.all()
    groups = GroupModel.query.all()
    users = db.session.query(UserModel.id, UserModel.name).all()
    rates = RateModel.query.all()
    fee_models = FeeModel.query.all()
    outputs = OutputModel.query.all()
    promotions = searchPVContentSql()

    return render_template("html/promotion/promotionManage.html", plats=plats, groups=groups, users=users, rates=rates,
                           feeModels=fee_models, outputs=outputs, promotions=promotions)


@bp.route("/data")
def data():
    promotion_data = searchTotalDataSql()
    message = {
        "counted": promotion_data[0].count,
        "liked": promotion_data[0].liked,
        "commented": promotion_data[0].commented,
        "collected": promotion_data[0].collected,
    }
    return jsonify({"status": "success", "message": message})


@bp.route("/dayData", methods=['GET', 'POST'])
def dayData():
    cycle = request.args.get("cycle")
    interval = request.args.get("interval")
    interval = int(interval) if interval else 30
    cycle = cycle.upper() if cycle else "D"
    promotion_data = searchTotalDataSql(interval=interval, group_by="1")
    promotion_data = promotionChartData(promotion_data, cycle=cycle,
                                        values=["count", "liked", "commented", "collected"])
    return jsonify({"data": promotion_data})


@bp.route("/downFile")
def downFile():
    save_path = 'static/excel/推广批量上传模板.xlsx'
    makePVContentExcel(save_path)
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
            current_app.celery.send_task("writeFilePVContent", (save_path,))
            return jsonify({"status": "success", "message": "正在上传文件，是否出错请查看日志"})
        else:
            return jsonify({'status': 'failed', 'message': form.messages})
    else:
        return jsonify({"status": "failed", "message": "请上传正确的文件"})


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


def allowImageFile(filename):
    return '.' in filename and filename.split('.')[1].lower() in current_app.config.get('IMAGE_ALLOWED_EXTENSIONS')


def makeImgaName(promotionId, file):
    random_name = "".join([str(0) for i in range(0, 10 - len(promotionId))]) + str(promotionId)
    suffix = file.filename.split(".")[1]
    return random_name + "." + suffix
