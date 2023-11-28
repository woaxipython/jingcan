from shortuuid import uuid
from datetime import datetime

from sqlalchemy import Index

from exts import db


class BrandModel(db.Model):
    __tablename__ = "brand"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    search_id = db.Column(db.String(100), default=uuid)
    name = db.Column(db.String(10), nullable=False)
    createtime = db.Column(db.DateTime, default=datetime.now)


class PrtypeModel(db.Model):
    __tablename__ = "prtype"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), nullable=False, unique=True)
    createTime = db.Column(db.DateTime, default=datetime.now)


# 平台
class PlatModel(db.Model):
    __tablename__ = 'plat'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    search_id = db.Column(db.String(100), default=uuid)
    name = db.Column(db.String(10), nullable=False)
    EH_name = db.Column(db.String(20))
    is_Store = db.Column(db.Boolean)
    is_Promotion = db.Column(db.Boolean)
    createtime = db.Column(db.DateTime, default=datetime.now)


class AtomCategoryModel(db.Model):
    __tablename__ = "atom_category"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    search_id = db.Column(db.String(100), default=uuid)
    name = db.Column(db.String(30), nullable=False)


class UnitModel(db.Model):
    __tablename__ = "unit"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    search_id = db.Column(db.String(100), default=uuid)
    name = db.Column(db.String(30), nullable=False)


# 合作模式：图文、视频等
class OutputModel(db.Model):
    __tablename__ = "output_mode"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50))
    createtime = db.Column(db.DateTime, default=datetime.now)


# 付费模式，纯佣金，付费、免费、佣金+付费等
class FeeModel(db.Model):
    __tablename__ = "feemodel"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50))
    createtime = db.Column(db.DateTime, default=datetime.now)


# 进度
class RateModel(db.Model):
    __tablename__ = "rate"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50))
    createtime = db.Column(db.DateTime, default=datetime.now)


# 店铺推广方式
class AdMethodModel(db.Model):
    __tablename__ = "admethod"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    search_id = db.Column(db.String(100), default=uuid)
    name = db.Column(db.String(50), nullable=False, unique=True)
    desc = db.Column(db.String(50))

    plat_id = db.Column(db.Integer, db.ForeignKey('plat.id'))
    plat = db.relationship("PlatModel", backref='admethods')


class CityModel(db.Model):
    __tablename__ = "city"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), nullable=False, unique=True)
    createTime = db.Column(db.DateTime, default=datetime.now)


class ProvinceModel(db.Model):
    __tablename__ = "province"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), nullable=False, unique=True)
    createTime = db.Column(db.DateTime, default=datetime.now)

    city_id = db.Column(db.Integer, db.ForeignKey("city.id"))
    city = db.relationship("CityModel", backref="provinces")


class CountyModel(db.Model):
    __tablename__ = "county"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), nullable=False, unique=True)
    createTime = db.Column(db.DateTime, default=datetime.now)

    province_id = db.Column(db.Integer, db.ForeignKey("province.id"))
    province = db.relationship("ProvinceModel", backref="counties")


class XhsTokenModel(db.Model):
    __tablename__ = "xhsToken"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    wechat = db.Column(db.String(30), nullable=False, unique=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    phone = db.Column(db.String(30), nullable=False, unique=True)
    status = db.Column(db.String(30), default="正常")
    createTime = db.Column(db.DateTime, default=datetime.now)


class DyTokenModel(db.Model):
    __tablename__ = "dyToken"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    wechat = db.Column(db.String(30), nullable=False, unique=True)
    name = db.Column(db.Text, nullable=False)
    webid = db.Column(db.Text, nullable=False,)
    msToken = db.Column(db.Text, nullable=False)
    phone = db.Column(db.String(30), nullable=False, unique=True)
    status = db.Column(db.String(30), default="正常")
    createTime = db.Column(db.DateTime, default=datetime.now)
