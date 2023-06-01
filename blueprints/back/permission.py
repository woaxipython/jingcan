from APP.SQLAPP.addEdit.dataWrite import writeSimpleModelData
from APP.SQLAPP.addEdit.permissionUser import writeNewPermission, writeNewRole, editRoleModel
from form.formValidate import PermissionModelForm, PermissionForm, RoleForm, EditRoleForm
from flask import Blueprint, request, render_template, jsonify
from models.user import PermissionCategoryModel, PermissionModel, RoleModel

bp = Blueprint("permission", __name__, url_prefix="/permission")


@bp.route("/manage")
def manage():
    perCategories = PermissionCategoryModel.query.all()
    permissions = PermissionModel.query.all()
    roles = RoleModel.query.all()
    return render_template("html/back/permissionManage.html", perCategories=perCategories, permissions=permissions,
                           roles=roles)


@bp.route("/newModel", methods=['POST'])
def newPermissionModel():
    form_dict = request.form.to_dict()
    print(form_dict)
    name = form_dict.get("newPermissinModel")
    form = PermissionModelForm(form_dict)
    if form.validate():
        return writeSimpleModelData(PermissionCategoryModel, name)
    else:
        return jsonify({"status": "failed", "message": form.messages})


@bp.route("/new", methods=['POST'])
def newPermission():
    form_dict = request.form.to_dict()
    cate = form_dict.get("permissionModel")
    name = form_dict.get("newPermissionName")
    form = PermissionForm(form_dict)
    if form.validate():
        return writeNewPermission(cate, name)
    else:
        return jsonify({"status": "failed", "message": form.messages})


@bp.route("/newRole", methods=['POST'])
def newRole():
    form_dict = request.get_json()
    print(form_dict)
    form = RoleForm(form_dict)
    if form.validate():
        return writeNewRole(form_dict)
    else:
        return jsonify({"status": "failed", "message": form.messages})


@bp.route("/editRole", methods=['POST'])
def editRole():
    form_dict = request.get_json()
    print(form_dict)
    form = EditRoleForm(form_dict)
    if form.validate():
        return editRoleModel(form_dict)
    else:
        return jsonify({"status": "failed", "message": form.messages})
