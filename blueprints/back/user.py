from APP.SQLAPP.addEdit.permissionUser import writeNewUser


from blueprints.promotionManage import allowImageFile
from form.formValidate import UserForm
from flask import Blueprint, request, render_template, jsonify

from models.back import CityModel
from models.user import RoleModel, UserModel

bp = Blueprint("user", __name__, url_prefix="/user")


@bp.route("/manage")
def manage():
    citys = CityModel.query.all()
    roles = RoleModel.query.all()
    users = UserModel.query.all()
    return render_template("html/back/userManage.html", citys=citys, roles=roles, users=users)


@bp.route("/newUser", methods=['POST'])
def newUser():
    form_dict = request.form.to_dict()
    print(form_dict)
    file = request.files.get("file")
    form = UserForm(form_dict)
    if form.validate():
        if file and allowImageFile:
            return writeNewUser(file, form_dict)
        else:
            return jsonify({"status": "failed", "message": "请上传头像图片"})
    else:
        return jsonify({"status": "success", "message": form.messages})
