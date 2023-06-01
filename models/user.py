from enum import Enum
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from exts import db
from shortuuid import uuid

role_permission_table = db.Table(
    "role_permission_table",
    db.Column("role_id", db.Integer, db.ForeignKey("role.id")),
    db.Column("permission_id", db.Integer, db.ForeignKey("permission.id"))
)


class PermissionCategoryModel(db.Model):
    __tablename__ = "permission_category"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), nullable=False, unique=True)


# 权限模型
class PermissionModel(db.Model):
    __tablename__ = "permission"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), nullable=False, unique=True)

    category_id = db.Column(db.Integer, db.ForeignKey("permission_category.id"))
    category = db.relationship("PermissionCategoryModel", backref="permissions")


class RoleModel(db.Model):
    __tablename__ = "role"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), nullable=False)
    desc = db.Column(db.String(200))
    create_time = db.Column(db.DateTime, default=datetime.now)
    permission = db.relationship("PermissionModel", secondary=role_permission_table,
                                 backref="roles")


class UserModel(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    search_id = db.Column(db.String(100), default=uuid)
    name = db.Column(db.String(10), nullable=False)
    phone = db.Column(db.String(20))
    wechat = db.Column(db.String(30), nullable=False)
    city = db.Column(db.String(10))
    province = db.Column(db.String(10))
    card = db.Column(db.String(20))
    address = db.Column(db.String(50))
    gender = db.Column(db.Integer)
    degree = db.Column(db.String(20))
    university = db.Column(db.String(20))
    account = db.Column(db.String(100), nullable=False, unique=True)
    _password = db.Column(db.String(200), nullable=False)
    cost = db.Column(db.Integer)
    # 头像，存储图片在服务器中保存的路径
    avatar = db.Column(db.String(200))
    # 签名
    remark = db.Column(db.String(200))
    jointime = db.Column(db.DateTime, default=datetime.now)
    # 是否可用
    status = db.Column(db.Boolean, default=True)

    # 外键
    role_id = db.Column(db.Integer, db.ForeignKey("role.id"))
    role = db.relationship("RoleModel", backref="users")

    def __init__(self, *args, **kwargs):
        if "password" in kwargs:
            self.password = kwargs.get("password")
            kwargs.pop("password")
        super(UserModel, self).__init__(*args, **kwargs)

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, row_password):
        self._password = generate_password_hash(row_password)

    def check_password(self, raw_password):
        result = check_password_hash(self.password, raw_password)
        return result

    def has_permission(self, permission):
        return permission in [permission.name for permission in self.role.permissions]
