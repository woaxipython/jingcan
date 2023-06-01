from shortuuid import uuid
from datetime import datetime
from exts import db


# 商品分为物料级、产品级、售卖级、组合级
# 物料是最小产品单位，本企业无法生产。由物料拆分组成产品，由产品组成售卖商品，由售卖商品组成组合。组合更类似于一个用于分析的集合。
# atom与product之间的关系，一个atom可以组成多个product，一个product可能由多个不同atom的不同数量组成，因此是多对多且由quantity列
class AtomSalesModel(db.Model):
    __tablename__ = "atoms_sales"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    atomid = db.Column(db.Integer, db.ForeignKey("atom.id"))
    saleid = db.Column(db.Integer, db.ForeignKey("sale.id"))
    quantity = db.Column(db.Integer, )


class AtomSupplierModel(db.Model):
    __tablename__ = "atoms_supplier"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    atomid = db.Column(db.Integer, db.ForeignKey("atom.id"))
    supplierid = db.Column(db.Integer, db.ForeignKey("supplier.id"))


class SaleStoreModel(db.Model):
    __tablename__ = "sale_store"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    sale_id = db.Column(db.Integer, db.ForeignKey("sale.id"))
    store_id = db.Column(db.Integer, db.ForeignKey("store.id"))


# sales与Group之间的关系，一个sale可以组成多个group，一个group可以由多个sale组成，因此是多对多关系
class SalesGroupsModel(db.Model):
    __tablename__ = "sales_groups"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    sale_id = db.Column(db.Integer, db.ForeignKey("sale.id"))
    group_id = db.Column(db.Integer, db.ForeignKey("group.id"))


# 产品物料，直接采购的本企业无法生产的最小单位
class AtomModel(db.Model):
    __tablename__ = "atom"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    search_id = db.Column(db.String(100), default=uuid)
    name = db.Column(db.String(30), nullable=False)
    code = db.Column(db.String(10), nullable=False)
    cost = db.Column(db.Float, default=0)
    weight = db.Column(db.Float)
    quantity = db.Column(db.Integer, default=0)
    remark = db.Column(db.String(200))
    createtime = db.Column(db.DateTime, default=datetime.now)

    # 绑定商品与sku的关系，一个商品有多个SKU，一个SKU可以对应多个商品，因此是多对多关系
    sales = db.relationship('SaleModel', secondary=AtomSalesModel.__tablename__, backref='atoms')

    # Atom与供应商之间的关系
    suppliers = db.relationship('SupplierModel', secondary=AtomSupplierModel.__tablename__, backref='atoms')

    # Atom与品牌之间的关系
    brand_id = db.Column(db.Integer, db.ForeignKey('brand.id'))
    brand = db.relationship("BrandModel", backref='atoms')

    # 绑定与分类之间的分类关系，一个分类多个商品
    category_id = db.Column(db.Integer, db.ForeignKey('atom_category.id'))
    category = db.relationship("AtomCategoryModel", backref='atoms')

    # 单位
    unit_id = db.Column(db.Integer, db.ForeignKey('unit.id'))
    unit = db.relationship("UnitModel", backref="atoms")


# 售卖级商品，实际面向消费者进行售卖的SKU
class SaleModel(db.Model):
    __tablename__ = "sale"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    search_id = db.Column(db.String(100), default=uuid)
    name = db.Column(db.String(80))
    sale_name = db.Column(db.String(80), nullable=False)
    code = db.Column(db.String(30))
    price = db.Column(db.Float)
    cost = db.Column(db.Float, default=0) # 成本价
    createtime = db.Column(db.DateTime, default=datetime.now)

    # 绑定与group之间的关系
    group = db.relationship('GroupModel', secondary=SalesGroupsModel.__tablename__, backref='sales')

    # 绑定与店铺之间的关系
    store = db.relationship('StoreModel', secondary=SaleStoreModel.__tablename__, backref='sales')

    # SKU商品与品牌之间的关系
    brand_id = db.Column(db.Integer, db.ForeignKey('brand.id'))
    brand = db.relationship("BrandModel", backref='sales')


# 定义产品的大类，即
class GroupModel(db.Model):
    __tablename__ = 'group'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    search_id = db.Column(db.String(100), default=uuid)
    name = db.Column(db.String(30), nullable=False)
    code = db.Column(db.String(30), nullable=False)
    createtime = db.Column(db.DateTime, default=datetime.now)


class PurchaseModel(db.Model):
    __tablename__ = "purchase"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    search_id = db.Column(db.String(100), default=uuid)
    name = db.Column(db.String(40), nullable=False)
    freight = db.Column(db.Integer, nullable=False)
    other = db.Column(db.Integer, nullable=False)
    cost = db.Column(db.Float, nullable=False)
    remark = db.Column(db.String(30))
    createtime = db.Column(db.DateTime, default=datetime.now)

    # 采购员
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship("UserModel", backref='purchases')


class PurchaseAtomModel(db.Model):
    __tablename__ = "purchase-atom"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    search_id = db.Column(db.String(100), default=uuid)
    number = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Float, nullable=False)
    cost = db.Column(db.Float, nullable=False)
    createtime = db.Column(db.DateTime, default=datetime.now)

    # 原料
    atom_id = db.Column(db.Integer, db.ForeignKey('atom.id', ))
    atom = db.relationship('AtomModel', backref='purchase-atoms')

    # 采购
    purchase_id = db.Column(db.Integer, db.ForeignKey('purchase.id'))
    purchase = db.relationship('PurchaseModel', backref='purchase-atoms')

    # 供应商
    supplier_id = db.Column(db.Integer, db.ForeignKey('supplier.id'))
    supplier = db.relationship('SupplierModel', backref='purchase-atoms')


class SupplierModel(db.Model):
    __tablename__ = "supplier"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    search_id = db.Column(db.String(50), default=uuid)
    campany_name = db.Column(db.String(50), nullable=False)
    campany_simple_name = db.Column(db.String(50), nullable=False)
    name = db.Column(db.String(10))
    gender = db.Column(db.Integer)
    wechat = db.Column(db.String(20))
    age = db.Column(db.String(20))
    phone = db.Column(db.String(20))
    city = db.Column(db.String(10))
    province = db.Column(db.String(10))
    address = db.Column(db.String(100))
    remark = db.Column(db.String(100))
    createtime = db.Column(db.DateTime, default=datetime.now)

    # 物料成本记录与采购员之间的关系，一个采购员多个Atom
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship("UserModel", backref='suppliers')
