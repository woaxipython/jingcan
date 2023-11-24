from sqlalchemy import or_

from APP.Spyder.makeRealURL import MakeRealURL
from exts import db
from models.promotion import AccountModel
from models.promotiondata import PVContentModel


class ChangeSQL():
    def __init__(self):
        pass

    def changeContentLink(self):
        filters = [PVContentModel.content_link != None, PVContentModel.content_link != ""]
        entities = [PVContentModel.content_link]
        content_link_list = PVContentModel.query.filter(*filters).with_entities(*entities).all()
        # content_link_list = db.session.query(PVContentModel.content_link).first()
        for content_link in content_link_list:
            content_link = content_link[0]
            print(content_link)
            content_model = PVContentModel.query.filter_by(content_link=content_link).first()
            note_link = MakeRealURL().makePVContentURL(content_link)
            if note_link:
                content_id = MakeRealURL().makeContentID(note_link)
                content_model.content_link = note_link
                content_model.content_id = content_id
                content_model.status = "正常"
            else:
                content_model.status = "链接错误"
            db.session.commit()

    def changeAccountLink(self):
        filters = [AccountModel.profile_link != None, AccountModel.profile_link != ""]
        entities = [AccountModel.profile_link]
        account_link_list = AccountModel.query.filter(*filters).with_entities(*entities).all()
        for account_link in account_link_list:
            profile_link = account_link[0]
            print(111, profile_link)
            account_model = AccountModel.query.filter_by(profile_link=profile_link).first()
            account_link = MakeRealURL().makeAccountURL(profile_link)
            uid = "链接错误"
            if account_link:
                uid = MakeRealURL().makeAccountID(profile_link)
                account_model.profile_link = account_link
                account_model.account_id = uid
                account_model.status = "正常"
            else:
                account_model.status = "链接错误"
            # print(account_link,uid)
            db.session.commit()

    def changePlat(self):
        # pvcontent_lists = AccountModel.query.filter(AccountModel.profile_link != None).with_entities(
        #     AccountModel.profile_link, AccountModel.id).all()
        # for pvcontent_list in pvcontent_lists:
        #     print(pvcontent_list.profile_link)
        #     if "xiaohongshu" in pvcontent_list.profile_link:
        #         plat_model = PlatModel.query.filter(PlatModel.name == "小红书").first()
        #         pn_model = AccountModel.query.filter(AccountModel.id == pvcontent_list.id).first()
        #         pn_model.plat_id = plat_model.id
        #         db.session.add(pn_model)
        #         db.session.commit()
        #     elif "douyin" in pvcontent_list.profile_link:
        #         plat_model = PlatModel.query.filter(PlatModel.name == "抖音").first()
        #         pn_model = AccountModel.query.filter(AccountModel.id == pvcontent_list.id).first()
        #         pn_model.plat_id = plat_model.id
        #         db.session.add(pn_model)
        #         db.session.commit()
        pvcontent_lists = PVContentModel.query.filter(PVContentModel.account_id == None).with_entities(
            PVContentModel.content_link, PVContentModel.id).all()
        for pvcontent_list in pvcontent_lists:
            print(pvcontent_list.content_link)
            if "xiaohongshu" in pvcontent_list.content_link:
                plat_model = PlatModel.query.filter(PlatModel.name == "小红书").first()
            elif "douyin" in pvcontent_list.content_link:
                plat_model = PlatModel.query.filter(PlatModel.name == "抖音").first()
            pv_model = PVContentModel.query.filter(PVContentModel.id == pvcontent_list.id).first()
            account_model = AccountModel()
            account_model.plat = plat_model
            account_model.profile_link = pvcontent_list.content_link
            account_model.self = "素人"

            pv_model.account = account_model
            db.session.add(account_model)
            db.session.add(pv_model)
            db.session.commit()


if __name__ == '__main__':
    ChangeSQL().changeContentLink()
