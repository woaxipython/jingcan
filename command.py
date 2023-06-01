import click
from sqlalchemy import and_

from APP.createCodeId import createAtomCode
from exts import db
from models.back import UnitModel, AtomCategoryModel, BrandModel, OutputModel, FeeModel, PlatModel, RateModel, \
    XhsTokenModel, DyTokenModel
from models.product import SupplierModel, AtomModel
from models.store import HandOrderCategory
from models.user import PermissionCategoryModel, PermissionModel, RoleModel, UserModel


def baseSelectModel():
    Initialization()


class Initialization(object):
    def __init__(self):
        self.createPermissionModel()
        self.createPermission()
        self.createRole()
        self.createAdmin()
        self.baseSelectModel()
        self.createSupplier()
        self.createAtom()

    def createPermissionModel(self):
        permission_category_model = PermissionCategoryModel(name="品牌")
        db.session.add(permission_category_model)
        db.session.commit()
        click.echo("权限分类创建成功")

    def createPermission(self):
        model_id = PermissionCategoryModel.query.filter_by(name="品牌").first().id
        permission_model = PermissionModel(name="万明", category_id=model_id)
        db.session.add(permission_model)
        db.session.commit()
        click.echo("权限创建成功")

    def createRole(self):
        permission = PermissionModel.query.filter(PermissionModel.name == "万明").first()
        role_model = RoleModel(name="管理员", desc="拥有网站所有权限")
        role_model.permission.append(permission)
        db.session.add(role_model)
        db.session.commit()
        click.echo("角色创建成功")

    def createAdmin(self):
        user_list = [
            {"search_id": "000001", "name": "赵延腾", "phone": "15369140121", "wechat": "qhzzeg", "city": "深圳市",
             "province": "广东省", "card": "130535199202073513", "address": "广东省深圳市龙岗区黄金山公园",
             "gender": "1",
             "degree": "本科", "university": "石家庄学院", "account": "qhzzeg@qq.com", "cost": "20000", "remark": "",
             "avatar": "100004.png", "password": "123456", "role_id": "1"},
            {"search_id": "000002", "name": "邹丽平", "phone": "15369140122", "wechat": "qhzzeg1", "city": "深圳市",
             "province": "广东省", "card": "130535199202073514", "address": "广东省深圳市龙岗区黄金山公园",
             "gender": "0",
             "degree": "本科", "university": "广东工业大学", "account": "qhzzeg1@qq.com", "cost": "10000", "remark": "",
             "avatar": "100004.png", "password": "123456", "role_id": "1"},
            {"search_id": "000003", "name": "胡晓丹", "phone": "15369140123", "wechat": "qhzzeg2", "city": "深圳市",
             "province": "广东省", "card": "130535199202073515", "address": "广东省深圳市龙岗区黄金山公园",
             "gender": "0",
             "degree": "本科", "university": "广东工业大学", "account": "qhzzeg2@qq.com", "cost": "12000", "remark": "",
             "avatar": "100004.png", "password": "123456", "role_id": "1"},
            {"search_id": "000004", "name": "赵婷", "phone": "15369140124", "wechat": "qhzzeg3", "city": "深圳市",
             "province": "广东省", "card": "130535199202073516", "address": "广东省深圳市龙岗区黄金山公园",
             "gender": "0",
             "degree": "本科", "university": "广东工业大学", "account": "qhzzeg3@qq.com", "cost": "10000", "remark": "",
             "avatar": "100004.png", "password": "123456", "role_id": "1"},
            {"search_id": "000005", "name": "番茄", "phone": "15369140125", "wechat": "qhzzeg4", "city": "深圳市",
             "province": "广东省", "card": "130535199202073517", "address": "广东省深圳市龙岗区黄金山公园",
             "gender": "0",
             "degree": "本科", "university": "广东工业大学", "account": "qhzzeg4@qq.com", "cost": "7500", "remark": "",
             "avatar": "100004.png", "password": "123456", "role_id": "1"},
            {"search_id": "000006", "name": "蓝希茹", "phone": "15369140126", "wechat": "qhzzeg5", "city": "深圳市",
             "province": "广东省", "card": "130535199202073518", "address": "广东省深圳市龙岗区黄金山公园",
             "gender": "0",
             "degree": "本科", "university": "广东工业大学", "account": "qhzzeg5@qq.com", "cost": "15000", "remark": "",
             "avatar": "100004.png", "password": "123456", "role_id": "1"},
        ]
        for user in user_list:
            user_model = UserModel(search_id=user.get("search_id"), name=user.get("name"), phone=user.get("phone"),
                                   wechat=user.get("wechat"), city=user.get("city"), province=user.get("province"),
                                   card=user.get("card"), address=user.get("address"),
                                   gender=user.get("gender"), degree=user.get("degree"),
                                   university=user.get("university"),
                                   account=user.get("account"),
                                   cost=user.get("cost"), remark=user.get("remark"),
                                   avatar=user.get("avatar"), password=user.get("password"),
                                   role_id=user.get("role_id"),
                                   )
            db.session.add(user_model)
            db.session.commit()
            click.echo(f'{user.get("name")}用户数据添加成功！')
        click.echo('用户数据添加成功！')

    def baseSelectModel(self):
        unit_model_1 = UnitModel(name="个")
        unit_model_2 = UnitModel(name="克")
        pr_category_1 = AtomCategoryModel(name="速干胶")
        pr_category_2 = AtomCategoryModel(name="树脂胶")
        pr_category_3 = AtomCategoryModel(name="包装辅料")
        pr_category_4 = AtomCategoryModel(name="固体胶")
        pr_category_5 = AtomCategoryModel(name="除胶剂")
        brand_model = BrandModel(name="万明")
        output_model = OutputModel(name="单篇图文")
        output_model_2 = OutputModel(name="图文合集")
        fee_model_1 = FeeModel(name="付费")
        fee_model_2 = FeeModel(name="纯佣")
        fee_model_3 = FeeModel(name="付费-佣金")

        plat_model_1 = PlatModel(name="小红书", is_Promotion=True)
        plat_model_2 = PlatModel(name="抖音", is_Promotion=True)
        rate_model_1 = RateModel(name="已约稿")
        rate_model_2 = RateModel(name="已发稿")
        rate_model_3 = RateModel(name="已付款")
        xhs_token_1 = XhsTokenModel(name="wxmp.873198bd-3612-49f7-b68b-1bd2eb1743a9", phone="15369140121",
                                    wechat="15369140121", )
        xhs_token_2 = XhsTokenModel(name="wxmp.2ecad65f-cab0-4ce1-936c-993adf9bf5eb", phone="17665250217",
                                    wechat="17665250217", )
        dy_token = DyTokenModel(
            name="ttwid=1%7CNvLn_dFZxi5e7vG7FHjiNooA_0VOzam6PJZ77OPdfiM%7C1681889128%7C2cc1a98c7532fc3194aeffe9238bc6a422a3dba39a6d5d4abf8116d851a26158; passport_csrf_token=b8e30d7d38b232c46b41fefe0c471d17; passport_csrf_token_default=b8e30d7d38b232c46b41fefe0c471d17; s_v_web_id=verify_lgndd2ax_s5kCld9F_I7TG_4LTK_8y1V_CMpjQQjgH1qC; pwa2=%223%7C0%22; d_ticket=ec7e699b5c2118fcd3faaa84e70b895b72c94; passport_assist_user=Cjz1O9l9Az1Q55mknWxfoYEGxOvHZqZev1FgFZo_usknPvGPOG1sLLVGaAbMwJzdwcvOsXsAEvmUWzCxOggaSAo8PUytSvd7xKs6k0od6pjbnw1D5wd29-rQH_BDqoh8y4K-GP9yujAB2-ClQgdEzwARmcRmypj1fHlPQe-TEK27sQ0Yia_WVCIBA6nd_N0%3D; n_mh=acm93QdnGeokQ8P9OssEFwOxgViwjjf-3wI379AUXj0; sso_auth_status=1e8efa73012bd7f252e39d07c634a9cc; sso_auth_status_ss=1e8efa73012bd7f252e39d07c634a9cc; sso_uid_tt=e46edc4ec726a056f711db0e1a8bb60c; sso_uid_tt_ss=e46edc4ec726a056f711db0e1a8bb60c; toutiao_sso_user=263c5d87974c6ba4fa2f2dc6482ea097; toutiao_sso_user_ss=263c5d87974c6ba4fa2f2dc6482ea097; sid_ucp_sso_v1=1.0.0-KDBhNWY2MTAxOWRjMzA0NDYyMjdjYjgwOTlkNGUzYjNkNDcxNGUwYWMKHQjAgNWO4wIQl5eYowYY7zEgDDDy4aHVBTgCQPEHGgJobCIgMjYzYzVkODc5NzRjNmJhNGZhMmYyZGM2NDgyZWEwOTc; ssid_ucp_sso_v1=1.0.0-KDBhNWY2MTAxOWRjMzA0NDYyMjdjYjgwOTlkNGUzYjNkNDcxNGUwYWMKHQjAgNWO4wIQl5eYowYY7zEgDDDy4aHVBTgCQPEHGgJobCIgMjYzYzVkODc5NzRjNmJhNGZhMmYyZGM2NDgyZWEwOTc; odin_tt=ac36a113358aa14bb2aa885d2dc483a3c7918f55e4ed76cf4ad982fcb128c943fee90a255e6f434be3ec5e586083a711; passport_auth_status=f79ac2e6db0d7c4e7caca42ee1061f04%2Cb81ba07f3de81cc75f02101940062756; passport_auth_status_ss=f79ac2e6db0d7c4e7caca42ee1061f04%2Cb81ba07f3de81cc75f02101940062756; uid_tt=9bc02b6263804a3f5495c4c9205a625c; uid_tt_ss=9bc02b6263804a3f5495c4c9205a625c; sid_tt=d1aad2c5dd6505edf1820b01e608a1e9; sessionid=d1aad2c5dd6505edf1820b01e608a1e9; sessionid_ss=d1aad2c5dd6505edf1820b01e608a1e9; LOGIN_STATUS=1; store-region=cn-gd; store-region-src=uid; sid_guard=d1aad2c5dd6505edf1820b01e608a1e9%7C1684409243%7C5183999%7CMon%2C+17-Jul-2023+11%3A27%3A22+GMT; sid_ucp_v1=1.0.0-KGFiZDU1OGJjN2RlNWExMjAwZjUwMDVkNTVjNDU4YzUzMDYzOTQ3OTYKGQjAgNWO4wIQm5eYowYY7zEgDDgCQPEHSAQaAmxmIiBkMWFhZDJjNWRkNjUwNWVkZjE4MjBiMDFlNjA4YTFlOQ; ssid_ucp_v1=1.0.0-KGFiZDU1OGJjN2RlNWExMjAwZjUwMDVkNTVjNDU4YzUzMDYzOTQ3OTYKGQjAgNWO4wIQm5eYowYY7zEgDDgCQPEHSAQaAmxmIiBkMWFhZDJjNWRkNjUwNWVkZjE4MjBiMDFlNjA4YTFlOQ; publish_badge_show_info=%220%2C0%2C0%2C1685342250339%22; strategyABtestKey=%221685342250.351%22; FOLLOW_LIVE_POINT_INFO=%22MS4wLjABAAAA9Ax-pVKjsUPUNdV-gbVq5OBjCe9HrIGwrNnNrTUP6pQ%2F1685376000000%2F0%2F0%2F1685354882652%22; FOLLOW_NUMBER_YELLOW_POINT_INFO=%22MS4wLjABAAAA9Ax-pVKjsUPUNdV-gbVq5OBjCe9HrIGwrNnNrTUP6pQ%2F1685376000000%2F0%2F1685354282652%2F0%22; tt_scid=coc4X4gQsKw5QDI8yN.1.-uaKrRyxY6gfOifN9u7h1Tg062Q2nW5P3uLiZ-mlHQpaa52; download_guide=%223%2F20230529%2F0%22; __ac_nonce=06474846d004841e5c5cf; __ac_signature=_02B4Z6wo00f01FpzHkQAAIDA2nHkB.aYGKRaUxrAAHLvR23K3O5VJ4WuXgJSvPuo.VZj6fVr08kK8IskwFbTjejT-j5sEAjV.tPIziLJCAyN0xFHjPY2XSeWd1k.ObN3pBVBiEW9rg8pgVlY4a; douyin.com; VIDEO_FILTER_MEMO_SELECT=%7B%22expireTime%22%3A1685962479784%2C%22type%22%3A1%7D; home_can_add_dy_2_desktop=%221%22; passport_fe_beating_status=true; msToken=GOJLPOLGnB9_p-tMKRKc8ezbiIupWfBv6ObOS_zQKYQUEvkn7lnZoSQP5C3PMPVrqjMdtG1tXSs_o649LYz1b5BsEJM4hADNuNHp1LAW5kCFG7xztAfczb6lRwJHkYI=; msToken=at0yyAfbn0vX3HkcBRZXziJMS1Uh0rwD88KaCcHspT5reYwggteBb202tGHh0kf6Zw20iuHiin1lVg-7c8WoWFxqi6-Lq4A0Jsuxh2xjl_oZbKbsRhYT-trSTpAXMhA=; csrf_session_id=55aee1a83c7e0582bf6de8b09e58313d; bd_ticket_guard_client_data=eyJiZC10aWNrZXQtZ3VhcmQtdmVyc2lvbiI6MiwiYmQtdGlja2V0LWd1YXJkLWl0ZXJhdGlvbi12ZXJzaW9uIjoxLCJiZC10aWNrZXQtZ3VhcmQtY2xpZW50LWNlcnQiOiItLS0tLUJFR0lOIENFUlRJRklDQVRFLS0tLS1cbk1JSUNFekNDQWJxZ0F3SUJBZ0lVUE5UKzhjSzdER3RldHcya0YyQTVSNGx6SkFBd0NnWUlLb1pJemowRUF3SXdcbk1URUxNQWtHQTFVRUJoTUNRMDR4SWpBZ0JnTlZCQU1NR1hScFkydGxkRjluZFdGeVpGOWpZVjlsWTJSellWOHlcbk5UWXdIaGNOTWpNd05URTRNVEV5TnpJd1doY05Nek13TlRFNE1Ua3lOekl3V2pBbk1Rc3dDUVlEVlFRR0V3SkRcblRqRVlNQllHQTFVRUF3d1BZbVJmZEdsamEyVjBYMmQxWVhKa01Ga3dFd1lIS29aSXpqMENBUVlJS29aSXpqMERcbkFRY0RRZ0FFeCtDVDNETy9BWkdNTXAwS1hBYjlqcThwTUE5T2RGQUExODFqZUZqK2wwa1d4S0ZQUDBURm9GRndcbno3L1RhbEZKVXNDSnBEdjJuTGQ5clBjY0FiY28zYU9CdVRDQnRqQU9CZ05WSFE4QkFmOEVCQU1DQmFBd01RWURcblZSMGxCQ293S0FZSUt3WUJCUVVIQXdFR0NDc0dBUVVGQndNQ0JnZ3JCZ0VGQlFjREF3WUlLd1lCQlFVSEF3UXdcbktRWURWUjBPQkNJRUlOcWVRSDI2NFMvRlBJazlVRHdvVjhRa3FVL0JXTkh6M2gwRkl4bGlBSFQzTUNzR0ExVWRcbkl3UWtNQ0tBSURLbForcU9aRWdTamN4T1RVQjdjeFNiUjIxVGVxVFJnTmQ1bEpkN0lrZURNQmtHQTFVZEVRUVNcbk1CQ0NEbmQzZHk1a2IzVjVhVzR1WTI5dE1Bb0dDQ3FHU000OUJBTUNBMGNBTUVRQ0lFZ1pJNUJzSFZlcXJBWDZcbmFvaUJSQXhSN29kVDhmTTJ0RTdMNGNVeXFkQmJBaUJlTk1pZzUwdVJEMjFoVzhHRTcvOXdHR3I2Q0hJK1BSVUFcbjlGSFlMZzA3a2c9PVxuLS0tLS1FTkQgQ0VSVElGSUNBVEUtLS0tLVxuIn0=")
        hand_order_model_1 = HandOrderCategory(name="售后补发")
        hand_order_model_2 = HandOrderCategory(name="快递丢失")
        hand_order_model_3 = HandOrderCategory(name="发错货")
        hand_order_model_4 = HandOrderCategory(name="漏发货")
        hand_order_model_5 = HandOrderCategory(name="分销单")
        db.session.add_all(
            [unit_model_1, unit_model_2, pr_category_1, pr_category_2, brand_model, output_model, fee_model_1,
             fee_model_2, plat_model_1, plat_model_2, rate_model_1, hand_order_model_1, hand_order_model_2,
             hand_order_model_3, hand_order_model_4, hand_order_model_5, pr_category_3, pr_category_4, pr_category_5,
             output_model_2, xhs_token_1, xhs_token_2, fee_model_3, rate_model_2, rate_model_3,
             dy_token])
        db.session.commit()
        click.echo('基础数据添加成功！')

    def createSupplier(self):
        dis_model = SupplierModel(campany_name="深圳协平粘胶制业",
                                  campany_simple_name="协平粘胶",
                                  name="张三",
                                  gender="1",
                                  age="20岁-30岁",
                                  wechat="zhangsan",
                                  phone="15369140121", city="深圳市", province="广东省",
                                  address="广东省深圳市龙岗区黄金山公园",
                                  remark="", user_id="1")
        db.session.add(dis_model)
        db.session.commit()
        click.echo('供应商数据添加成功！')

    def createAtom(self):
        max_id = AtomModel.query.filter(
            and_(AtomModel.category_id == 1, AtomModel.brand_id == 1)).count() + 1
        atom_code = createAtomCode(1, 1, max_id)
        atom_model = AtomModel(name="手办胶水",
                               code=atom_code,
                               category_id=1,
                               unit_id=1,
                               brand_id=1,
                               weight=40,
                               remark="", )
        supplier = SupplierModel.query.get(1)
        atom_model.suppliers.append(supplier)
        db.session.add(atom_model)
        db.session.commit()
#
#
#
#
# def create_role():
#     # 运营
#     # 先改RoleModel模型，然后根据RoleMolde模型，来修改permissionMolde中的模型。实际写入的是中间件数据库
#     operator = RoleModel(name="老板", desc="这家公司的负责人，拥有所有权限")
#     operator.permission = PermissionModel.query.filter(
#         PermissionModel.name.in_([
#             PermissionEnum.BOSS,
#             PermissionEnum.OPERATION,
#             PermissionEnum.FINANCIAL,
#             PermissionEnum.MARKET,
#             PermissionEnum.SUPPLY,
#             PermissionEnum.CUSTOMERSERVICE,
#             PermissionEnum.AMAZON,
#         ])).all()
#     print(PermissionEnum.BOSS,
#           PermissionEnum.OPERATION,
#           PermissionEnum.FINANCIAL,
#           PermissionEnum.MARKET,
#           PermissionEnum.SUPPLY,
#           PermissionEnum.CUSTOMERSERVICE,
#           PermissionEnum.AMAZON, )
#     db.session.add(operator)
#     db.session.commit()
#     click.echo("角色添加成功")
#
#
# def create_blogger():
#     bloger = BloggerModel(weixin="1536914021")
#     click_command = []
#     click_command.append(bloger)
#     bloger.plat = PlatFormModel.query.filter(
#         PlatFormModel.name.in_([
#             "DOUYIN",
#         ])).all()
#     print(type(bloger.plat))
#     print(bloger.plat)
#     # 增加账号
#     account = AccountModel(name_id="15369140121", name="你的赵爸爸")
#     account.blog = bloger
#     account.plat = bloger.plat[0]
#     click_command.append(account)
#
#     # 增加图文
#     blog = PromotionDataModel(name="胶水的100种用法")
#
#     blog.blog = bloger
#     blog.account = account
#     blog.plat = bloger.plat[0]
#     click_command.append(blog)
#
#     db.session.add_all(click_command)
#     db.session.commit()
#     click.echo("测试成功")
