import os

from APP.DataCalculate.productSQLCal import DataSale
from APP.SQLAPP.addEdit.product import writeNewSupplierModel, writeNewAtomModel, writeNewPurchaseModel, \
    writeNewSaleModel, writeNewGroupModel, writeCondeStractFile, refreshSaleCost

from APP.SQLAPP.search.product import searchGroupModel, makeCodeStractFile, searchAtomModel, searchSaleModel

from blueprints.sale.saleManage import allExcelFile
from form.fileValidate import codeContractFileForm
from form.formValidate import AtomForm, SupplierForm, newPurchaseForm, newSaleForm, newGroupForm
from flask import Blueprint, request, current_app, render_template, send_file, \
    jsonify, redirect, url_for
from werkzeug.utils import secure_filename

from models.back import UnitModel, AtomCategoryModel, BrandModel, CityModel
from models.product import SupplierModel
from models.store import CodeStractModel
from models.user import UserModel

bp = Blueprint("product", __name__, url_prefix="/product")


@bp.route("/manage", methods=["GET", "POST"])
def manage():
    if request.method == "POST":
        form_dict = request.form.to_dict()
        atomNm = form_dict.get("searchAtomName", "").strip()
        atomCate = form_dict.get("searchAtomCategory", "")
        saleNm = form_dict.get("searchSaleName", "")
        saleC = form_dict.get("searchSaleC", "")
        groupNm = form_dict.get("searchGroupName", "")
    else:
        atomNm = ""
        atomCate = ""
        saleNm = ""
        groupNm = ""
        saleC = ""
    atoms = searchAtomModel(atomNm, atomCate)
    sales = searchSaleModel(saleNm, saleC)
    sales = DataSale(sales)
    groups = searchGroupModel(groupNm)
    citys = CityModel.query.all()
    users = UserModel.query.all()
    suppliers = SupplierModel.query.all()
    units = UnitModel.query.all()
    atom_categories = AtomCategoryModel.query.all()
    brands = BrandModel.query.all()
    constract_codes = CodeStractModel.query.all()
    return render_template("html/back/productManage.html", citys=citys, users=users, suppliers=suppliers, units=units,
                           atom_categories=atom_categories, brands=brands, atoms=atoms, sales=sales, groups=groups,
                           constract_codes=constract_codes)


@bp.route("/constractCode")
def FileCodeConstract():
    file = request.files.get("file")
    if file and allExcelFile(file.filename):
        filename = "product_code_" + secure_filename(file.filename)
        save_path = os.path.join(current_app.config['UPLOADED_FILES_DEST'], filename)
        file.save(save_path)
        print(save_path)
        form = codeContractFileForm(save_path)
        if form.validate():
            return writeCondeStractFile(save_path)
        else:
            return jsonify({'status': 'failed', 'message': form.messages})
    else:
        return jsonify({"status": "failed", "message": "请上传正确的文件"})


@bp.route("/downFile")
def downFile():
    save_path = 'static/excel/编码对照表模板.xlsx'
    makeCodeStractFile(save_path)
    return send_file(save_path, as_attachment=True)


@bp.route("/newAtom", methods=['POST'])
def newAtom():
    form_dict = request.form.to_dict()
    print(form_dict)
    form = AtomForm(form_dict)
    if form.validate():
        return writeNewAtomModel(form_dict)
    else:
        return jsonify({"status": "failed", "message": form.messages})


@bp.route("/searchAtom")
def searchAtom():
    name = request.args.get("name")
    category_id = request.args.get("category_id")
    return redirect(url_for("back.productManage", atomNm=name, atomCate=category_id))


@bp.route("/newSaleProduct", methods=['POST'])
def newSaleProduct():
    form_dict = request.get_json()
    form = newSaleForm(form_dict)
    if form.validate():
        return writeNewSaleModel(form_dict)
    else:
        return jsonify({"status": "failed", "message": form.messages})


@bp.route("/newGroupProduct", methods=['POST'])
def newGroupProduct():
    form_dict = request.get_json()
    print(form_dict)
    form = newGroupForm(form_dict)
    if form.validate():
        return writeNewGroupModel(form_dict)
    else:
        return jsonify({"status": "failed", "message": form.messages})


@bp.route("/newSupplier", methods=['POST'])
def newSupplier():
    form_dict = request.form.to_dict()
    form = SupplierForm(form_dict)
    print(form_dict)
    if form.validate():
        return writeNewSupplierModel(form_dict)
    else:
        return jsonify({"status": "failed", "message": form.messages})


@bp.route("/newPurchase", methods=['POST'])
def newPurchase():
    form_dict = request.get_json()
    print(form_dict)
    form = newPurchaseForm(form_dict)
    if form.validate():
        write_result = writeNewPurchaseModel(form_dict)
        if write_result["status"] == "success":
            return jsonify(refreshSaleCost(form_dict))
        else:
            return jsonify(write_result)
    else:
        return jsonify({"status": "failed", "message": form.messages})
