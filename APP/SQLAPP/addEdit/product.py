from flask import jsonify
from sqlalchemy import func, and_, or_

from APP.DataCalculate.CalCulate import CalPurchaseCost, CalAtomCost
from APP.createCodeId import createAtomCode, createSaleCode, createGroupCode
from exts import db
from models.back import AtomCategoryModel, UnitModel, \
    BrandModel
from models.product import SaleModel, SupplierModel, AtomModel, PurchaseModel, PurchaseAtomModel, GroupModel, \
    AtomSalesModel
from models.store import CodeStractModel
from models.user import UserModel
from openpyxl.reader.excel import load_workbook


def writeNewSupplierModel(form_dict):
    user_model = UserModel.query.get(form_dict.get("newSupplierUser"))
    if not user_model:
        return jsonify({"status": "failed", "message": "没有该联络人"})
    else:
        dis_model = SupplierModel.query.filter_by(campany_name=form_dict.get("newSupplierCampany")).first()
        dis_model2 = SupplierModel.query.filter_by(campany_simple_name=form_dict.get("newSupplierSimpleName")).first()
        if dis_model or dis_model2:
            return jsonify({"status": "failed", "message": "不能添加！该供应商已存在"})
        else:
            dis_model = SupplierModel(campany_name=form_dict.get("newSupplierCampany"),
                                      campany_simple_name=form_dict.get("newSupplierSimpleName"),
                                      name=form_dict.get("newSupplierName"),
                                      gender=form_dict.get("newSupplierGender"),
                                      age=form_dict.get("newSupplierAge"),
                                      wechat=form_dict.get("newSupplierWechat"),
                                      phone=form_dict.get("newSupplierPhone"), city=form_dict.get("newSupplierCity"),
                                      province=form_dict.get("newSupplierProvince"),
                                      address=form_dict.get("newSupplierAddress"), remark=form_dict.get("remark"))
            dis_model.user = user_model
            db.session.add(dis_model)
            db.session.commit()
            return jsonify({"status": "success", "message": "新增成功"})


def writeNewAtomModel(form_dict):
    category_model = AtomCategoryModel.query.get(form_dict.get("newAtomCategory"))
    if not category_model:
        return jsonify({"status": "failed", "message": "没有该分类"})
    unit_model = UnitModel.query.get(form_dict.get("newAtomUnit"))
    if not unit_model:
        return jsonify({"status": "failed", "message": "没有该单位"})
    supplier_model = SupplierModel.query.get(form_dict.get("newAtomSupplier"))
    if not supplier_model:
        return jsonify({"status": "failed", "message": "没有该供应商"})
    brand_model = BrandModel.query.get(form_dict.get("newAtomBrand"))
    if not brand_model:
        return jsonify({"status": "failed", "message": "没有该品牌"})
    atom_model = AtomModel.query.filter_by(name=form_dict.get("newAtomName")).first()
    if atom_model:
        return jsonify({"status": "failed", "message": "该商品已存在"})
    else:
        max_id = AtomModel.query.filter(
            and_(AtomModel.category == category_model, AtomModel.brand == brand_model)).count() + 1
        atom_code = createAtomCode(form_dict.get("newAtomCategory"), form_dict.get("newAtomBrand"), max_id)
        atom_model = AtomModel(name=form_dict.get("newAtomName"),
                               code=atom_code,
                               category=category_model,
                               unit=unit_model,
                               brand=brand_model,
                               weight=form_dict.get("newAtomWeight"),
                               remark=form_dict.get("remark"))
        atom_model.suppliers.append(supplier_model)
        db.session.add(atom_model)
        db.session.commit()
        return jsonify({"status": "success", "message": "新增成功"})


def writeNewPurchaseModel(form_dict):
    pr_id_list = [purchases['atomId'] for purchases in form_dict['purchaseList']]
    atoms = AtomModel.query.filter(AtomModel.id.in_(pr_id_list)).all()
    if not atoms:
        return {"status": "failed", "message": "没有该商品"}
    user = UserModel.query.filter().get(form_dict['newPurchaseUser'])
    if not user:
        return {"status": "failed", "message": "没有该联络人"}
    now_atom_dict = {}

    # 获取当前采购单的商品信息，用于计算采购单成本
    for atom in atoms:
        now_atom_dict["prid" + str(atom.id)] = {
            "id": atom.id,
            "quantity": atom.quantity or "0",
            "cost": atom.cost or "0",
        }
    new_atom_dict = CalPurchaseCost(form_dict)

    # 计算采购单成本
    refresh_atoms = CalAtomCost(new_purchase_dict=new_atom_dict, now_atom_dict=now_atom_dict)

    purchase_name = PurchaseModel.query.filter(PurchaseModel.name == form_dict['newPurchaseName']).first()
    if purchase_name:
        return {"status": "failed", "message": "该采购单已存在"}
    else:
        purchase_model = PurchaseModel(name=form_dict['newPurchaseName'], freight=form_dict['newPurchaseFreight'],
                                       other=form_dict['newPurchaseOther'], cost=form_dict['totalCost'],
                                       remark=form_dict['remark'],
                                       user=user)
        db.session.add(purchase_model)

        # 更新商品库存和成本
        for i in range(len(refresh_atoms)):
            atoms_model = AtomModel.query.get(refresh_atoms[i]['id'])
            atoms_model.cost = refresh_atoms[i]['cost']
            atoms_model.quantity = refresh_atoms[i]['quantity']
            db.session.add(atoms_model)
        # 写入采购单商品
        for purchase_atoms in form_dict['purchaseList']:
            supplier_model = SupplierModel.query.get(purchase_atoms['supplierId'])
            if not supplier_model:
                return {"status": "failed", "message": "没有该供应商"}
            atom_model = AtomModel.query.get(purchase_atoms['atomId'])
            if not atom_model:
                return {"status": "failed", "message": "没有该商品"}
            purchase_atom = PurchaseAtomModel(atom=atom_model, purchase=purchase_model, supplier=supplier_model,
                                              number=purchase_atoms['number'], price=purchase_atoms['unitPrice'],
                                              cost=purchase_atoms['TotalPrice'])
            db.session.add(purchase_atom)
            db.session.commit()
        return {"status": "success", "message": "新增成功"}


def refreshSaleCost(form_dict):
    pr_id_list = [purchases['atomId'] for purchases in form_dict['purchaseList']]
    atoms = AtomModel.query.filter(AtomModel.id.in_(pr_id_list)).all()
    for aotom_model in atoms:
        for sale in aotom_model.sales:
            cost = 0
            for atom in sale.atoms:
                atom_cost = atom.cost or 0
                quantity = AtomSalesModel.query.filter_by(atomid=atom.id, saleid=sale.id).first().quantity
                cost += round(atom_cost * quantity, 2)
            sale.cost = cost
            db.session.add(sale)
    db.session.commit()
    return {"status": "success", "message": "新增成功"}


def writeNewSaleModel(form_dict):
    atom_cost = 0
    sale_model = SaleModel.query.filter(
        or_(SaleModel.name == form_dict['newSaleName'], SaleModel.sale_name == form_dict['newSaleSkuName'])).first()
    if sale_model:
        return jsonify({"status": "failed", "message": "该产品已存在，请勿重复添加"})
    for atoms in form_dict['atomlist']:
        atom_model = AtomModel.query.filter_by(code=atoms['atomCode']).first()  # 获取商品
        if not atom_model:
            return jsonify({"status": "failed", "message": "没有该商品"})  # 没有该商品
    max_id = db.session.query(func.max(SaleModel.id)).scalar() or 0 + 1
    code = createSaleCode(max_id)
    atom_list = []
    sale_model = SaleModel(name=form_dict['newSaleName'], sale_name=form_dict['newSaleSkuName'], code=code,
                           price=form_dict['newSalePrice'])
    db.session.add(sale_model)
    db.session.commit()
    saleid = SaleModel.query.filter_by(code=code).first().id
    print(sale_model.id)
    for atoms in form_dict['atomlist']:
        atom_model = AtomModel.query.filter_by(code=atoms['atomCode']).first()  # 获取商品
        atom_cost += round(atom_model.cost * int(atoms['number']), 2)  # 计算成本
        atomsale = AtomSalesModel(atomid=atom_model.id, saleid=saleid, quantity=atoms['number'])
        atom_list.append(atomsale)  # 添加商品
    sale_model.cost = atom_cost

    db.session.add_all(atom_list)
    db.session.commit()
    return jsonify({"status": "success", "message": "新增成功"})


def writeNewGroupModel(form_dict):
    group_model = GroupModel.query.filter_by(name=form_dict['newGroupName']).first()
    if group_model:
        return jsonify({"status": "failed", "message": "该商品组已存在，请勿重复添加"})
    else:
        sale_list = []
        max_id = db.session.query(func.max(GroupModel.id)).scalar() or 0 + 1
        code = createGroupCode(max_id)
        for sales in form_dict['saleList']:
            sale_model = SaleModel.query.filter_by(code=sales['saleCode']).first()
            if not sale_model:
                return jsonify({"status": "failed", "message": "没有该产品,请先添加产品"})
            sale_list.append(sale_model)
        group_model = GroupModel(name=form_dict['newGroupName'], code=code)
        group_model.sales = sale_list
        db.session.add(group_model)
        db.session.commit()
        return jsonify({"status": "success", "message": "新增成功"})


def writeCondeStractFile(save_path):
    workbook = load_workbook(save_path)
    sheet = workbook.active
    error_message = []
    for row in sheet.rows:
        if row[0].row == 1:
            continue
        sale_name = row[0].value
        sale_code = row[1].value
        sale_model = SaleModel.query.filter_by(code=sale_code).first()
        if not sale_model:
            error_message.append("第" + str(row[1].column) + "列的产品不存在")
            continue
        stract_model = CodeStractModel.query.filter_by(name=sale_name).first()
        if not stract_model:
            stract_model = CodeStractModel(name=sale_name)
        stract_model.sale = sale_model
        db.session.add(stract_model)
        db.session.commit()
    if error_message:
        return jsonify({"status": "failed", "message": error_message})
    else:
        return jsonify({"status": "success", "message": "新增成功"})
