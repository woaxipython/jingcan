import os
from flask import jsonify, current_app
from sqlalchemy import func, and_, or_
from APP.SQLAPP.addEdit.dataWrite import generate_Number_string, makeRandomName
from APP.Spyder.KdzsSpyder import KuaiDiZhuShouSpyder
from exts import db
from models.user import UserModel, PermissionModel, RoleModel, PermissionCategoryModel

kdzs = KuaiDiZhuShouSpyder()


def writeNewUser(file, form_dict):
    max_id = db.session.query(func.max(UserModel.id)).scalar()
    max_id = max_id + 1 if max_id else 1
    search_id = generate_Number_string(6, max_id)
    filename = makeRandomName(file.filename, max_id, 6)
    save_path = os.path.join(current_app.config['UPLOADED_IMAGE_DEST'], filename)
    file.save(save_path)
    name_model = UserModel.query.filter_by(name=form_dict.get("newUserName")).first()
    wechat_model = UserModel.query.filter_by(wechat=form_dict.get("newUserWechat")).first()
    card_model = UserModel.query.filter_by(card=form_dict.get("newUserCards")).first()
    if not name_model and not wechat_model and not card_model:
        user_model = UserModel(search_id=search_id, name=form_dict.get("newUserName"),
                               phone=form_dict.get("newUserPhone"), wechat=form_dict.get("newUserWechat"),
                               city=form_dict.get("newUserCity"), province=form_dict.get("newUserProvince"),
                               card=form_dict.get("newUserCards"), address=form_dict.get("newUserAddress"),
                               gender=form_dict.get("newUserGender"), degree=form_dict.get("newUserDegree"),
                               university=form_dict.get("newUserUniversity"),
                               account=form_dict.get("newUserEmail"),
                               cost=form_dict.get("newUserCost"), remark=form_dict.get("remark"),
                               avatar=filename, password=form_dict.get("newUserPassword"),
                               role_id=form_dict.get("newUserRole"),
                               )
        db.session.add(user_model)
        db.session.commit()
        return jsonify({"status": "success", "message": "新增成功"})
    else:
        return jsonify({"status": "failed", "message": "用户名或微信号或身份证号已存在"})


def editRoleModel(form_dict):
    permission = PermissionModel.query.filter(PermissionModel.id.in_(form_dict.get("permission"))).all()
    role_model = RoleModel.query.get(form_dict.get("editRoleId"))
    if not role_model:
        return jsonify({"status": "failed", "message": "没有该角色"})
    else:
        print(role_model)
        role_model.permission = []
        role_model.permission = permission
        db.session.add(role_model)
        db.session.commit()
        return jsonify({"status": "success", "message": "修改成功"})


def writeNewRole(form_dict):
    permission = PermissionModel.query.filter(PermissionModel.id.in_(form_dict.get("permission"))).all()
    role_model = RoleModel.query.filter_by(name=form_dict.get("newRoleName")).first()
    if not role_model:
        role_model = RoleModel(name=form_dict.get("newRoleName"), desc=form_dict.get("newRoleDesc"))
    else:
        role_model.permission.clear()
    role_model.permission = permission
    db.session.add(role_model)
    db.session.commit()
    return jsonify({"status": "success", "message": "新增成功"})


def writeNewPermission(cate, name):
    cate_model = PermissionCategoryModel.query.get(cate)
    if cate_model:
        permission = PermissionModel.query.filter_by(name=name).first()
        if permission:
            return jsonify({"status": "failed", "message": "名称已存在"})
        else:
            permission = PermissionModel(name=name)
            permission.category = cate_model
            db.session.add(permission)
            db.session.commit()
            return jsonify({"status": "success", "message": "新增成功"})
    else:
        return jsonify({"status": "failed", "message": "分类模型不存在"})
