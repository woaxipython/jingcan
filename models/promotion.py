from shortuuid import uuid
from datetime import datetime
from exts import db


# 合作_平台中间件
class PromotionPlatsModel(db.Model):
    __tablename__ = "promotion_plats"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    promotion_id = db.Column(db.Integer, db.ForeignKey("promotion.id"))
    plat_id = db.Column(db.Integer, db.ForeignKey("plat.id"))


# 合作_账号中间件
class PromotionAcountsModel(db.Model):
    __tablename__ = "promotion_acount"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    promotion_id = db.Column(db.Integer, db.ForeignKey("promotion.id"))
    acount_id = db.Column(db.Integer, db.ForeignKey("account.id"))


# 合作_商品中间件
class PromotionGroupsModel(db.Model):
    __tablename__ = "promotion_groups"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    promotion_id = db.Column(db.Integer, db.ForeignKey("promotion.id"))
    group_id = db.Column(db.Integer, db.ForeignKey("group.id"))


# 合作，一次合作一个博主，一次合作多个账号，多个图文
class PromotionModel(db.Model):
    __tablename__ = "promotion"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    search_id = db.Column(db.String(100), default=uuid)
    fee = db.Column(db.Float())
    commission = db.Column(db.Float())
    remark = db.Column(db.String(100))
    feeImgLink = db.Column(db.String(100))
    orderstatus = db.Column(db.Integer)
    createtime = db.Column(db.DateTime, default=datetime.now)


    # 合作与博主之间的多对多关系，一个合作有一个博主，一个博主多个合作
    bloger_id = db.Column(db.Integer, db.ForeignKey('bloger.id'))
    bloger = db.relationship('BlogerModel', backref='promotions')

    # 进度
    rate_id = db.Column(db.Integer, db.ForeignKey('rate.id'))
    rate = db.relationship("RateModel", backref='promotions')

    # 进度
    feeModel_id = db.Column(db.Integer, db.ForeignKey('feemodel.id'))
    feeModel = db.relationship("FeeModel", backref='promotions')

    # 推广与负责人之间的关系，一个负责人多个推广
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship("UserModel", backref='promotions')

    # 推广与品牌之间的关系，一个品牌多个推广
    brand_id = db.Column(db.Integer, db.ForeignKey('brand.id'))
    brand = db.relationship("BrandModel", backref='promotions')

    # 合作与产品之间的多对多关系，一个商品有多个合作，一个合作多个商品
    group = db.relationship('GroupModel', secondary=PromotionGroupsModel.__tablename__, backref='promotions')

    order_id = db.Column(db.Integer, db.ForeignKey('parent_order.id'))
    order = db.relationship('ParentOrderModel', backref='promotions', uselist=False)


# 博主
class BlogerModel(db.Model):
    __tablename__ = 'bloger'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    search_id = db.Column(db.String(100), default=uuid)
    name = db.Column(db.String(50))
    wechat = db.Column(db.String(30))
    phone = db.Column(db.String(20))
    address = db.Column(db.String(50))
    createtime = db.Column(db.DateTime, default=datetime.now)


# 账号
class AccountModel(db.Model):
    __tablename__ = 'account'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    search_id = db.Column(db.String(100), default=uuid)
    self = db.Column(db.String(10))
    nickname = db.Column(db.String(50))
    fans = db.Column(db.Integer)
    follow = db.Column(db.Integer)
    gender = db.Column(db.Integer)
    account_id = db.Column(db.String(50))
    notes = db.Column(db.Integer)
    boards = db.Column(db.String(50))
    location = db.Column(db.String(30))
    collected = db.Column(db.Integer)
    ave_collected = db.Column(db.Float)
    collected_rate = db.Column(db.Float)
    desc = db.Column(db.String(200))
    liked = db.Column(db.Integer)
    ave_liked = db.Column(db.Float)
    liked_rate = db.Column(db.Float)
    officialVerifyName = db.Column(db.String(30))
    spyder_url = db.Column(db.String(200))
    profile_link = db.Column(db.String(200))

    # 对应博主
    bloger_id = db.Column(db.Integer, db.ForeignKey('bloger.id'))
    bloger = db.relationship('BlogerModel', backref='accounts')

    # 对应平台
    plat_id = db.Column(db.Integer, db.ForeignKey('plat.id'))
    plat = db.relationship('PlatModel', backref='accounts')
