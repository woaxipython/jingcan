import os
from datetime import datetime, timedelta
from flask import jsonify, current_app
from werkzeug.utils import secure_filename
from APP.Spyder.KdzsSpyder import KuaiDiZhuShouSpyder
from APP.Spyder.getAddress import getAddress
from exts import db
from models.back import CityModel, ProvinceModel, CountyModel

kdzs = KuaiDiZhuShouSpyder()


def writeXhsTokenModel(Model, name, phone, wechat):
    model = Model.query.filter_by(phone=phone).first()
    if model:
        model.name = name
        model.wechat = wechat
        db.session.add(model)
        db.session.commit()
    else:
        model = Model(name=name, phone=phone, wechat=wechat)
        db.session.add(model)
        db.session.commit()
    return jsonify({"status": "success", "message": "新增成功"})


def writeSimpleModelData(Model, name):
    model = Model.query.filter_by(name=name).first()
    if model:
        return jsonify({"status": "failed", "message": "名称已存在"})
    else:
        model = Model(name=name)
        db.session.add(model)
        db.session.commit()
        return jsonify({"status": "success", "message": "新增成功"})


def writeNewPromotionPlatModel(Model, name):
    model = Model.query.filter_by(name=name).first()
    if model:
        model.is_Promotion = True
        db.session.add(model)
        db.session.commit()
        return jsonify({"status": "failed", "message": "已经添加为促销平台"})
    else:
        model = Model(name=name)
        model.is_Promotion = True
        db.session.add(model)
        db.session.commit()
        return jsonify({"status": "success", "message": "新增成功"})


def writeLocationModel():
    address_lids = getAddress()
    for address in address_lids:
        print(address)
        city, province, county = address
        city_model = CityModel.query.filter_by(name=city).first()
        if not city_model:
            city_model = CityModel(name=city)
        province_model = ProvinceModel.query.filter_by(name=province).first()
        if not province_model:
            province_model = ProvinceModel(name=province)
        county_model = CountyModel.query.filter_by(name=county).first()
        if not county_model:
            county_model = CountyModel(name=county)
        province_model.city = city_model
        county_model.province = province_model
        db.session.add(county_model)
        db.session.commit()


def dealDate(now="", zero="", end_date="", start_date="", length=""):
    if now:
        endDate = datetime.now()
        startDate = (endDate - timedelta(days=int(length))).strftime(
            '%Y-%m-%d %H:%M')
        endDate = endDate.strftime('%Y-%m-%d %H:%M')
    else:
        endDate = datetime.strptime(end_date, '%Y-%m-%dT%H:%M').strftime('%Y-%m-%d %H:%M')
        startDate = datetime.strptime(start_date, '%Y-%m-%dT%H:%M').strftime('%Y-%m-%d %H:%M')
    if zero:
        endDate = endDate + ":00"
        startDate = startDate + ":00"
    return startDate, endDate


# 生成随机字符串
def generate_Number_string(length, code):
    if len(str(code)) < length:
        number = 1
        for i in range(1, length):
            number = number * 10
        code = number + int(code)
    return str(code)


def makeRandomName(file_name, id, length):
    random_name = generate_Number_string(length, id)
    filename, suffix = secure_filename(file_name).split(".")
    return random_name + "." + suffix
