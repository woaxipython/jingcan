from shortuuid import uuid
from datetime import datetime
from exts import db


# 图文
class PVContentModel(db.Model):
    __tablename__ = 'pvcontent'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    search_id = db.Column(db.String(100), default=uuid)

    title = db.Column(db.String(100))
    content_id = db.Column(db.Integer)
    desc = db.Column(db.String(500))
    liked = db.Column(db.Integer)
    collected = db.Column(db.Integer)
    commented = db.Column(db.Integer)
    forwarded = db.Column(db.Integer)
    content_link = db.Column(db.String(200))
    video_link = db.Column(db.String(200))
    spyder_url = db.Column(db.String(200))
    status = db.Column(db.String(20), default='正常')
    upload_time = db.Column(db.DateTime, )
    create_time = db.Column(db.DateTime, default=datetime.now)

    # 对应账号，一次合作多个图文
    account_id = db.Column(db.Integer, db.ForeignKey('account.id'))
    account = db.relationship('AccountModel', backref='pvcontents')

    # 对应合作，一次合作多个图文
    promotion_id = db.Column(db.Integer, db.ForeignKey('promotion.id'))
    promotion = db.relationship('PromotionModel', backref='pvcontents')

    # 产出模式
    output_id = db.Column(db.Integer, db.ForeignKey('output_mode.id'))
    output = db.relationship("OutputModel", backref='pvcontents', uselist=False)


# 评论内容
class CommentModel(db.Model):
    __tablename__ = "comment"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    search_id = db.Column(db.String(100), default=uuid)
    name = db.Column(db.String(30))
    upload_time = db.Column(db.DateTime, )
    title = db.Column(db.String(100))
    content = db.Column(db.Text)
    createtime = db.Column(db.DateTime, default=datetime.now)

    pvcontent_id = db.Column(db.Integer, db.ForeignKey('pvcontent.id'))
    pvcontent = db.relationship('PVContentModel', backref='comments')


# 图文数据数据库——每日更新1次
class PVDataModel(db.Model):
    __tablename__ = "pvdata"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    search_id = db.Column(db.String(100), nullable=False)
    liked = db.Column(db.Integer)
    collected = db.Column(db.Integer)
    commented = db.Column(db.Integer)
    forwarded = db.Column(db.Integer)
    createtime = db.Column(db.DateTime, default=datetime.now)

    # 图文与数据之间的关系，外键
    pvcontent_id = db.Column(db.Integer, db.ForeignKey('pvcontent.id'))
    pvcontent = db.relationship('PVContentModel', backref='pvdatas')


# 直播
class LiveingModel(db.Model):
    __tablename__ = 'liveing'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    search_id = db.Column(db.String(100), default=uuid)
    liveing_id = db.Column(db.Integer)
    title = db.Column(db.String(100))
    living_date = db.Column(db.DateTime, nullable=False)
    timelength = db.Column(db.Integer)
    createtime = db.Column(db.DateTime, default=datetime.now)

    # 对应合作，一次合作多个图文
    cooperation_id = db.Column(db.Integer, db.ForeignKey('promotion.id'))
    cooperation = db.relationship('PromotionModel', backref='liveings')
