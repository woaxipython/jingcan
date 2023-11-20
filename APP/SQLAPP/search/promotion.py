import random
from datetime import datetime, timedelta

import pandas as pd
from sqlalchemy import or_, func, Date, cast

from APP.DataCalculate.CalCulate import AccountBasicData
from APP.Spyder.DySpyder import DouYinSpyder
from APP.Spyder.XshSpyder import GetXhsSpyder
from exts import db
from flask import jsonify

from models.back import PlatModel, XhsTokenModel, DyTokenModel, RateModel, FeeModel, OutputModel, PrtypeModel
from models.product import GroupModel
from models.promotion import AccountModel, PromotionModel, BlogerModel, PromotionGroupsModel
from models.promotiondata import PVContentModel, PVDataModel
from models.store import ParentOrderModel
from models.user import UserModel

xhs = GetXhsSpyder()
dy = DouYinSpyder()


class GetPromotionModel():
    def __init__(self, end_date="", start_date="", interval=90, ):
        self.end_date = end_date
        self.start_date = start_date
        self.interval = interval
        self.makeDate()
        self.makeEntity()
        self.filters = [PromotionModel.createtime >= self.start_date, PromotionModel.createtime < self.end_date, ]

    def makeDate(self):
        self.end_date = datetime.strptime(self.end_date, "%Y-%m-%d") if self.end_date else datetime.now()
        self.start_date = datetime.strptime(self.start_date, "%Y-%m-%d") if self.start_date else \
            self.end_date - timedelta(days=self.interval)

    def makeEntity(self):
        self.entities = [
            PromotionModel.createtime.label('date'),
            GroupModel.name.label("group_name"),
            BlogerModel.wechat.label('bloger'),
            UserModel.name.label('user'),
            PromotionModel.fee.label('fee'),
            OutputModel.name.label('output'),
            RateModel.name.label('rate'),
            PlatModel.name.label('plat'),
            AccountModel.nickname.label('account'),
            PVContentModel.title.label('title'),
            PVContentModel.status.label('status'),
            PVContentModel.content_link.label('content_link'),
            PVContentModel.liked.label('liked'),
            PVContentModel.collected.label('collected'),
            PVContentModel.commented.label('commented'),
        ]

    def getSQlData(self):
        orders = db.session.query(PromotionModel, GroupModel).filter(*self.filters) \
            .join(PromotionGroupsModel, PromotionGroupsModel.promotion_id == PromotionModel.id) \
            .join(GroupModel, PromotionGroupsModel.group_id == GroupModel.id) \
            .join(PromotionModel.pvcontents) \
            .join(OutputModel) \
            .join(UserModel) \
            .join(BlogerModel) \
            .join(AccountModel) \
            .join(RateModel) \
            .join(PlatModel) \
            .with_entities(*self.entities).all()

        return orders


def searchPVContentSql(end_date=datetime.now().strftime("%Y-%m-%d"), self="", rate="", promotion_id="", wechat="",
                       interval=365, plat="",
                       prtype="", group="", group_=""):
    group_by = ["link"]
    interval = 365 if interval == 171 else interval
    end_date = datetime.strptime(end_date, "%Y-%m-%d")
    start_date = end_date - timedelta(days=interval)
    filters = [PVContentModel.create_time >= start_date, PVContentModel.create_time < end_date,
               PVContentModel.content_link != None,]

    filters.append(AccountModel.self == self) if self and self != "0" else filters
    filters.append(GroupModel.id == group) if group and group != "0" else filters
    filters.append(PrtypeModel.name == prtype) if prtype and prtype != "0" else filters
    filters.append(BlogerModel.wechat == wechat) if wechat else filters
    filters.append(PlatModel.name == plat) if plat else filters
    filters.append(PromotionModel.rate_id == rate) if rate and rate != "0" else filters
    filters = [PromotionModel.search_id == promotion_id] if promotion_id else filters
    group_by.extend(group_.split(",")) if group_ else group_by
    entities = [cast(PVContentModel.create_time, Date).label('date'),
                GroupModel.name.label('group'),
                AccountModel.nickname.label('account'),
                AccountModel.profile_link.label('profile_link'),
                AccountModel.self.label('self'),
                PVContentModel.title.label('title'),
                PVContentModel.search_id.label('id'),
                PVContentModel.content_link.label('link'),
                PVContentModel.liked.label('liked'),
                PVContentModel.commented.label('commented'),
                PVContentModel.forwarded.label('forwarded'),
                PVContentModel.collected.label('collected'),
                PVContentModel.video_link.label('video'),
                PlatModel.name.label('plat')]
    pvcontent_list = PVContentModel.query.filter(*filters).join(PVContentModel.account).join(
        AccountModel.plat).join(PVContentModel.promotion).join(PromotionModel.group).with_entities(*entities).group_by(
        *group_by).all()
    return pvcontent_list


def searchPVContentSql2(plat="", self="", group=""):
    group_by = []
    group_by.extend(group.split(",")) if group else group_by
    filters = [PVContentModel.content_link != None, or_(PVContentModel.status == "正常",PVContentModel.status==None)]
    filters.append(AccountModel.self == self) if self and self != "0" else filters
    filters.append(PlatModel.name == plat) if plat else filters
    entities = [
        AccountModel.profile_link.label('profile_link'),
        PVContentModel.content_link.label('link'),
        PlatModel.name.label('plat')]
    pvcontent_list = PVContentModel.query.filter(*filters).join(PVContentModel.account).join(
        AccountModel.plat).join(PVContentModel.promotion).join(PromotionModel.group).with_entities(*entities).group_by(
        "link").all()
    return pvcontent_list


def dictPromotionORM(promotion_ORM):
    data = []
    for promotion in promotion_ORM:
        promotion = {
            "id": promotion.id,
            "search_id": promotion.search_id,
            "fee": promotion.fee,
            "commission": promotion.commission,
            "feeImgLink": promotion.feeImgLink,
            'bloger': {'id': promotion.bloger.id, 'wechat': promotion.bloger.wechat},
            'account': [{'id': pvcontent.account.account_id,
                         'name': pvcontent.account.nickname,
                         'profile_link': pvcontent.account.profile_link,
                         'plat': {'id': pvcontent.account.plat.id,
                                  'name': pvcontent.account.plat.name}} for pvcontent in promotion.pvcontents],
            'pvcontent': [{'id': pvcontent.search_id, 'title': pvcontent.title, 'content_link': pvcontent.content_link,
                           'out_put': {'id': pvcontent.output.id,
                                       'name': pvcontent.output.name}} for pvcontent in promotion.pvcontents],
            'rate': {'id': promotion.rate.id, 'name': promotion.rate.name},
            'feeModel': {'id': promotion.feeModel.id, 'name': promotion.feeModel.name},
            'user': {'id': promotion.user.id, 'name': promotion.user.name},
            'group': [{'id': group.id, 'name': group.name} for group in promotion.group if group],
        }
        data.append(promotion)
    return data


class searchAccount(object):
    def __init__(self, form_dict):
        """ 初始化 """
        """
        profileLink: 账号链接 (必填) str
        platId: 平台id (必填) int
        nickname: 昵称 (必填) str
        """
        self.form_dict = form_dict
        self.error_message = []
        self.profile_result = {}
        self.plat_id = self.form_dict["platId"]
        self.plat_name = ""

    def checkExist(self):
        account_link = self.form_dict["profileLink"]
        account_model = AccountModel.query.filter_by(profile_link=account_link).first()
        if account_model:
            return True
        else:
            return False

    def check(self):

        self.plat_model = PlatModel.query.get(self.plat_id)
        if not self.plat_model:
            self.error_message.append("推广平台不存在，请确认或录入至手工录入平台")
            return False
        self.plat_name = self.plat_model.name
        return True

    def sypderAccount(self):
        profile_link = self.form_dict["profileLink"]
        token = xhsToken()

        if self.plat_name == "小红书":
            if not token:
                return {"status": "failed", "message": "正常小红书账号已用完，请联系管理员"}
            profile_result = xhs.getUserInfo(token=token, url=profile_link)  # 获取账号信息
        elif self.plat_name == "抖音":
            profile_result = dy.getUserInfo(token=dyToken(), url=profile_link)  # 获取账号信息
        else:
            return {"status": "failed", "message": "暂时无法获取该平台账号数据，请手动录入，或联系管理员录入"}  # 返回失败信息

        if profile_result["status"] == "failed":  # 获取失败
            return {"status": "failed", "message": profile_result["message"]}  # 返回失败信息
        elif profile_result["status"] == "1":  # 获取成功，但是账号不存在或触发验证
            if profile_result["message"] == "Spam":
                token_model = XhsTokenModel.query.filter_by(name=token).first()
                token_model.status = "触发验证"
                db.session.add(token_model)
                return {"status": "2", "message": "触发小红书验证"}
            else:
                return {"status": "failed", "message": "爬虫解析错误"}
        else:
            self.profile_result = AccountBasicData(profile_result["message"])  # 获取成功，返回账号基础数据
            return {"status": "success", "message": self.profile_result}  # 返回成功信息

    def writeAccount(self):
        account_model = AccountModel.query.filter_by(account_id=self.profile_result["account_id"]).first()
        if account_model:
            for key, value in self.profile_result.items(): setattr(account_model, key, value)
            account_model.plat = self.plat_model
        else:
            account_model = AccountModel(**self.profile_result)  # 实例化账号模型
            account_model.plat = self.plat_model
        db.session.add(account_model)
        db.session.commit()
        return {"status": "success", "message": self.profile_result}


class searchNotes(object):
    def __init__(self):
        """ 初始化 """
        """
        """

    def spyderXHSNote(self, note_link):
        token = xhsToken()
        if not token:
            return {"status": "4", "message": "正常小红书账号已用完，请联系管理员"}
        profile_result = xhs.getNoteInfo(token=token, url=note_link)
        if profile_result["status"] == "0":
            # 链接错误
            return {"status": "0", "message": profile_result["message"]}
        elif profile_result["status"] == "3":
            return {"status": "3", "message": profile_result["message"]}
        elif profile_result["status"] == "2":
            token_model = XhsTokenModel.query.filter_by(name=token).first()
            if profile_result["message"] == "Spam":
                token_model.status = "触发验证"
                db.session.add(token_model)
                db.session.commit()
                return {"status": "2", "message": "token过期"}
            elif profile_result["message"] == "登录已过期":
                token_model.status = "登录已过期"
                db.session.add(token_model)
                db.session.commit()
                return {"status": "2", "message": "登录已过期"}
            else:
                return {"status": "2", "message": profile_result["message"]}
        else:
            return {"status": "1", "message": profile_result["message"]}

    def spyderDYNote(self, note_link):
        token = dyToken()
        if not token:
            return {"status": "4", "message": "正常抖音cookie已用完，请联系管理员"}
        profile_result = dy.getNoteInfo(token=token, url=note_link)

        if profile_result["status"] == "0":
            # 链接错误
            return {"status": "0", "message": profile_result["message"]}
        elif profile_result["status"] == "3":
            return {"status": "3", "message": profile_result["message"]}
        elif profile_result["status"] == "2":
            token_model = DyTokenModel.query.filter_by(name=token).first()
            token_model.status = "登录已过期"
            db.session.add(token_model)
            db.session.commit()
            return {"status": "2", "message": "登录已过期"}
        else:
            return {"status": "1", "message": profile_result["message"]}


def makePromotionExcel(save_path):
    writer = pd.ExcelWriter(save_path)

    columns = ["推广人", "博主微信", "账号主页链接", "平台", "推广产品，多个产品,隔开", "付费形式", "费用",
               "佣金", "图文链接", "产出形式", "合作时间", "账号自营"]
    df2 = pd.DataFrame(columns=columns)
    df2.to_excel(writer, sheet_name="推广模板", index=False)

    feeModel = FeeModel.query.all()
    fee_list = []
    for fee in feeModel:
        fee_list.append(fee.name)
    fee_df = pd.DataFrame(fee_list, columns=["费用类型"])
    fee_df.to_excel(writer, sheet_name="费用类型", index=False)
    platModel = PlatModel.query.all()
    plat_list = []
    for plat in platModel:
        plat_list.append(plat.name)
    plat_df = pd.DataFrame(plat_list, columns=["推广平台"])
    plat_df.to_excel(writer, sheet_name="推广平台", index=False)
    outputModel = OutputModel.query.all()
    output_list = []
    for output in outputModel:
        output_list.append(output.name)
    output_df = pd.DataFrame(output_list, columns=["输出类型"])
    output_df.to_excel(writer, sheet_name="输出类型", index=False)
    userModel = UserModel.query.all()
    user_list = []
    for user in userModel:
        user_list.append(user.name)
    user_df = pd.DataFrame(user_list, columns=["推广员可选"])
    user_df.to_excel(writer, sheet_name="推广员可选", index=False)
    productModel = GroupModel.query.all()
    product_list = []
    for product in productModel:
        product_list.append(product.name)
    product_df = pd.DataFrame(product_list, columns=["产品可选"])
    product_df.to_excel(writer, sheet_name="产品可选", index=False)

    # 激活指定的工作表
    workbook = writer.book
    worksheet = writer.sheets['推广模板']
    worksheet.active = True
    writer.close()


def xhsToken():
    token_list = db.session.query(XhsTokenModel.name).filter_by(status="正常").all()
    token_list = [token[0] for token in token_list]
    if not token_list:
        return None
    else:
        return random.choice(token_list)


def dyToken():
    token_list = db.session.query(DyTokenModel.name).filter_by(status="正常").all()
    token_list = [token[0] for token in token_list]
    if not token_list:
        return None
    else:
        return random.choice(token_list)
