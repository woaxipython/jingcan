import random
from datetime import datetime, timedelta

import pandas as pd
from sqlalchemy import or_, func, Date, cast, and_

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


# class GetPromotionModel():
#     def __init__(self, end_date="", start_date="", interval=90, ):
#         self.end_date = end_date
#         self.start_date = start_date
#         self.interval = interval
#         self.makeDate()
#         self.makeEntity()
#         self.filters = [PromotionModel.createtime >= self.start_date, PromotionModel.createtime < self.end_date, ]
#
#     def makeDate(self):
#         self.end_date = datetime.strptime(self.end_date, "%Y-%m-%d") if self.end_date else datetime.now()
#         self.start_date = datetime.strptime(self.start_date, "%Y-%m-%d") if self.start_date else \
#             self.end_date - timedelta(days=self.interval)
#
#     def makeEntity(self):
#         self.entities = [
#             PromotionModel.createtime.label('date'),
#             GroupModel.name.label("group_name"),
#             BlogerModel.wechat.label('bloger'),
#             UserModel.name.label('user'),
#             PromotionModel.fee.label('fee'),
#             OutputModel.name.label('output'),
#             RateModel.name.label('rate'),
#             PlatModel.name.label('plat'),
#             AccountModel.nickname.label('account'),
#             PVContentModel.title.label('title'),
#             PVContentModel.status.label('status'),
#             PVContentModel.content_link.label('content_link'),
#             PVContentModel.liked.label('liked'),
#             PVContentModel.collected.label('collected'),
#             PVContentModel.commented.label('commented'),
#         ]
#
#     def getSQlData(self):
#         orders = db.session.query(PromotionModel, GroupModel).filter(*self.filters) \
#             .join(PromotionGroupsModel, PromotionGroupsModel.promotion_id == PromotionModel.id) \
#             .join(GroupModel, PromotionGroupsModel.group_id == GroupModel.id) \
#             .join(PromotionModel.pvcontents) \
#             .join(OutputModel) \
#             .join(UserModel) \
#             .join(BlogerModel) \
#             .join(AccountModel) \
#             .join(RateModel) \
#             .join(PlatModel) \
#             .with_entities(*self.entities).all()
#
#         return orders


def searchPVContentSql(end_date=datetime.now().strftime("%Y-%m-%d"), self="",
                       interval=365, plat="", nickname="", liked_s=-1, liked_e=200000000,
                       commented_s=-1, commented_e=200000000,
                       collected_s=-1, collected_e=200000000,
                       contenttype="", group=""):
    interval = 365 if interval == 171 else interval
    end_date = datetime.strptime(end_date, "%Y-%m-%d")
    start_date = end_date - timedelta(days=interval)
    print(plat)
    filters = [
        PVContentModel.liked >= liked_s, PVContentModel.liked < liked_e,
        PVContentModel.commented >= commented_s, PVContentModel.commented < commented_e,
        PVContentModel.collected >= collected_s, PVContentModel.collected < collected_e,
        PVContentModel.upload_time >= start_date,
        PVContentModel.upload_time < end_date,
        PVContentModel.upload_time != None,
        PVContentModel.content_link != None]

    filters.append(AccountModel.self == self) if self and self != "0" else filters
    filters.append(AccountModel.id == nickname) if nickname and nickname != "0" else filters
    filters.append(GroupModel.id == group) if group and group != "0" else filters
    filters.append(PlatModel.name == plat) if plat else filters

    filters.append(PVContentModel.contenttype == contenttype) if contenttype and contenttype != "0" else filters
    filters.append(PVContentModel.contenttype != None) if contenttype and contenttype != "0" else filters

    entities = [cast(PVContentModel.upload_time, Date).label('date'),
                AccountModel.self.label('self'),
                AccountModel.nickname.label('account'),
                AccountModel.profile_link.label('profile_link'),
                PVContentModel.title.label('title'),
                PVContentModel.content_id.label('content_id'),
                PVContentModel.id.label('search_id'),
                PVContentModel.content_link.label('link'),
                PVContentModel.liked.label('liked'),
                PVContentModel.commented.label('commented'),
                PVContentModel.forwarded.label('forwarded'),
                PVContentModel.collected.label('collected'),
                PVContentModel.video_link.label('video'),
                PVContentModel.imageList.label('imageList'),
                PVContentModel.contenttype.label('contenttype'),
                PVContentModel.attention.label('attention'),
                PlatModel.name.label('plat')]
    pvcontent_list = PVContentModel.query.filter(*filters).join(PVContentModel.plat).join(PVContentModel.account).with_entities(*entities) \
        .order_by(PVContentModel.liked.desc()).distinct().all()
    return pvcontent_list


def searchPVContentSql2(plat="", attention=""):
    filters = [PVContentModel.content_link != None,
               or_(PVContentModel.status == "正常", PVContentModel.status == None),
               ]
    if attention == "all":
        attention_filter = or_(PVContentModel.attention == 1, PVContentModel.attention == None,
                               PVContentModel.attention == 0, PVContentModel.attention == 2)
    elif attention == "0":
        attention_filter = PVContentModel.attention == 0
    elif attention == "1":
        attention_filter = PVContentModel.attention == 1
    elif attention == "2":
        attention_filter = PVContentModel.attention == 2
    elif attention == "3":
        attention_filter = or_(PVContentModel.attention == 1, PVContentModel.attention == 2)
    elif attention == "4":
        attention_filter = PVContentModel.attention == None
    else:
        attention_filter = PVContentModel.attention == 1
    filters.append(attention_filter)
    filters.append(PlatModel.name == plat) if plat else filters
    entities = [
        PVContentModel.content_link.label('link'),
        PlatModel.name.label('plat')]
    pvcontent_list = PVContentModel.query.filter(*filters).join(PVContentModel.plat).with_entities(*entities).all()
    return pvcontent_list


def searchAccountSql2(plat="", attention=""):
    filters = [AccountModel.profile_link != None,
               or_(AccountModel.status == "正常", AccountModel.status == None),
               ]
    # filters = [PVContentModel.content_link != None, or_(PVContentModel.status == "正常", PVContentModel.status == None)]
    if attention == "all":
        attention_filter = or_(AccountModel.attention == 1, AccountModel.attention == None,
                               AccountModel.attention == 0, AccountModel.attention == 2)
    elif attention == "0":
        attention_filter = AccountModel.attention == 0
    elif attention == "1":
        attention_filter = AccountModel.attention == 1
    elif attention == "2":
        attention_filter = AccountModel.attention == 2
    elif attention == "3":
        attention_filter = or_(AccountModel.attention == 1, AccountModel.attention == 2)
    elif attention == "4":
        attention_filter = AccountModel.attention == None
    else:
        attention_filter = AccountModel.attention == 1
    filters.append(attention_filter)
    filters.append(PlatModel.name == plat) if plat else filters
    entities = [
        AccountModel.profile_link.label('link'),
        PlatModel.name.label('plat')]
    account_list = AccountModel.query.filter(*filters).join(
        AccountModel.plat).with_entities(*entities).group_by(
        "link").all()
    return account_list


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
    def __init__(self, ):
        """ 初始化 """
        """
        profileLink: 账号链接 (必填) str
        platId: 平台id (必填) int
        nickname: 昵称 (必填) str
        """

    def __account_confirm(self, profile_result, profile_link, token, plat):
        if profile_result["status"] == "0":
            # 链接错误
            return {"status": "0", "message": profile_result["message"]}
        elif profile_result["status"] == "3":
            return {"status": "3", "message": profile_result["message"]}
        elif profile_result["status"] == "2":
            token_model = DyTokenModel.query.filter_by(
                name=token).first() if plat == "抖音" else XhsTokenModel.query.filter_by(
                name=token).first()
            if profile_result["message"] == "Spam":
                token_model.status = "触发验证"  # 未验证
                token_model.save()
                return {"status": "2", "message": profile_result["message"]}
            elif profile_result["message"] == "登录已过期":
                token_model.status = "登录已过期"
                db.session.add(token_model)
                db.session.commit()
                result = self.sypderXHSAccount(profile_link)
                return result
            else:
                return {"status": "2", "message": profile_result["message"]}
        else:
            print(profile_result["message"]['nickname'])
            return {"status": "1", "message": profile_result["message"]}

    def spyderDYAccount(self, profile_link):
        token, msToken, webid = dyToken()
        if not token:
            return {"status": "4", "message": "正常抖音账号已用完，请联系管理员"}
        profile_result = dy.getUserInfo(token=token, url=profile_link, webid=webid, msToken=msToken)  # 获取账号信息
        return self.__account_confirm(profile_result, profile_link, token, "抖音")

    def sypderXHSAccount(self, profile_link):
        token = xhsToken()
        if not token:
            return {"status": "4", "message": "正常小红书账号已用完，请联系管理员"}
        profile_result = xhs.getUserInfo(token=token, url=profile_link)  # 获取账号信息
        return self.__account_confirm(profile_result, profile_link, token, "小红书")


class searchAccountNotes(object):
    def __init__(self):
        """ 初始化 """
        """
        """

    def spyderXHSAccountNote(self, profile_link, page):
        token = xhsToken()
        if not token:
            yield {"status": "4", "message": "正常小红书账号已用完，请联系管理员"}
        profile_results = xhs.getUserNoteList(token=token, page=page, url=profile_link)
        for profile_result in profile_results:
            has_more = profile_result.get("has_more")
            max_cursor = profile_result.get("max_cursor")
            info = {"status": "0", "message": profile_result["message"], "has_more": has_more, "max_cursor": max_cursor}
            if profile_result["status"] == "0":
                info["status"] = "0"
                # 链接错误
                yield info
            elif profile_result["status"] == "3":
                info["status"] = "3"
                yield info
            elif profile_result["status"] == "2":
                token_model = XhsTokenModel.query.filter_by(name=token).first()
                if profile_result["message"] == "Spam":
                    token_model.status = "触发验证"  # 未验证
                    db.session.add(token_model)
                    db.session.commit()
                    info["status"] = "2"
                    yield info
                elif profile_result["message"] == "登录已过期":
                    token_model.status = "登录已过期"
                    db.session.add(token_model)
                    db.session.commit()
                    info["status"] = "2"
                    yield info
                else:
                    info["status"] = "2"
                    yield info

            else:
                print(profile_result["message"]['title'])
                info["status"] = "1"
                yield info

    def spyderDYAccountNote(self, profile_link, max_cursor):
        token, msToken, webid = dyToken()
        if not token:
            yield {"status": "4", "message": "正常抖音账号已用完，请联系管理员"}
        profile_results = dy.getUserNoteList(token, webid, msToken, url=profile_link, max_cursor=max_cursor)

        for profile_result in profile_results:
            has_more = profile_result.get("has_more")
            max_cursor = profile_result.get("max_cursor")
            info = {"status": "0", "message": profile_result["message"], "has_more": has_more, "max_cursor": max_cursor}
            if profile_result["status"] == "0":
                info["status"] = "0"
                # 链接错误
                yield info
            elif profile_result["status"] == "3":
                info["status"] = "3"
                yield info
            elif profile_result["status"] == "2":
                token_model = DyTokenModel.query.filter_by(name=token).first()
                if profile_result["message"] == "Spam":
                    token_model.status = "触发验证"  # 未验证
                    db.session.add(token_model)
                    db.session.commit()
                    info["status"] = "2"
                    yield info
                elif profile_result["message"] == "登录已过期":
                    token_model.status = "登录已过期"
                    db.session.add(token_model)
                    db.session.commit()
                    info["status"] = "2"
                    yield info
                else:
                    info["status"] = "2"
                    yield info

            else:
                print(profile_result["message"]['title'])
                info["status"] = "1"
                yield info


class searchNotes(object):
    def __init__(self):
        """ 初始化 """
        """
        """

    def __note_confirm(self, profile_result, note_link, token, plat):
        info = {"status": "0", "message": profile_result["message"]}
        if profile_result["status"] == "0":
            # 链接错误
            return {"status": "0", "message": profile_result["message"]}
        elif profile_result["status"] == "3":
            return {"status": "3", "message": profile_result["message"]}
        elif profile_result["status"] == "2":
            token_model = XhsTokenModel.query.filter_by(
                name=token).first() if plat == "小红书" else DyTokenModel.query.filter_by(
                name=token).first()
            if profile_result["message"] == "Spam":
                token_model.status = "触发验证"
                db.session.add(token_model)
                db.session.commit()
                result = self.spyderXHSNote(note_link)
                return result
            elif profile_result["message"] == "登录已过期":
                token_model.status = "登录已过期"
                db.session.add(token_model)
                db.session.commit()
                result = self.spyderXHSNote(note_link)
                return result
            else:
                return {"status": "2", "message": profile_result["message"]}
        else:
            print(profile_result["message"]['title'])
            return {"status": "1", "message": profile_result["message"]}

    def spyderXHSNote(self, note_link):
        token = xhsToken()
        if not token:
            return {"status": "4", "message": "正常小红书账号已用完，请联系管理员"}
        profile_result = xhs.getNoteInfo(token=token, url=note_link)
        return self.__note_confirm(profile_result, note_link, token, "小红书")

    def spyderDYNote(self, note_link):
        token, msToken, webid = dyToken()
        if not token:
            return {"status": "4", "message": "正常抖音cookie已用完，请联系管理员"}
        profile_result = dy.getNoteInfo(token=token, url=note_link, webid=webid, msToken=msToken)
        return self.__note_confirm(profile_result, note_link, token, "抖音")


def makePVContentExcel(save_path):
    writer = pd.ExcelWriter(save_path)

    columns = ["推广产品", "*图文链接"]
    df2 = pd.DataFrame(columns=columns)
    df2.to_excel(writer, sheet_name="推广模板", index=False)
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
    token_list = db.session.query(DyTokenModel.name, DyTokenModel.msToken, DyTokenModel.webid).filter_by(
        status="正常").all()
    token_list = [(token.name, token.msToken, token.webid) for token in token_list]
    if not token_list:
        return None
    else:
        token, msToken, webid = random.choice(token_list)
        return token, msToken, webid
