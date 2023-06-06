import time
import random

from flask import jsonify
from openpyxl.reader.excel import load_workbook
from sqlalchemy import func, or_

from APP.SQLAPP.addEdit.dataWrite import generate_Number_string
from APP.SQLAPP.search.promotion import searchAccount, searchNotes
from exts import db
from models.back import RateModel, PlatModel, FeeModel, OutputModel
from models.product import GroupModel
from models.promotion import PromotionModel, BlogerModel, AccountModel
from models.promotiondata import PVContentModel
from models.store import OrderModel, ParentOrderModel
from models.user import UserModel


class writePromotionFee(object):
    def __init__(self, form_dict, save_path=""):
        """传入的form_dict前端传入的数据，字典格式，包含了所有的数据"""
        """
        editPromotionId:    ——>  promotion_id 推广id int
        editPromotionOrderId:  ——>  order_id 订单id str
        editPromotionCheck:  ——>  orderstatus 订单状态 str "0" or "1"
        save_path:  ——>  feeImgLink 保存路径 str
        """
        self.form_dict = form_dict
        self.error_message = []
        self.save_path = save_path
        self.search_id = self.form_dict.get("editPromotionId")
        self.order_id = self.form_dict.get("editPromotionOrderId")
        self.order_status = self.form_dict.get("editPromotionCheck")

    def check(self):
        """检查数据是否合法"""
        promotion_model = PromotionModel.query.filter_by(search_id=self.search_id).first()
        if not promotion_model:
            self.error_message.append("没有该推广记录，可尝试刷新页面")
        if self.order_status == "1":
            order_model = OrderModel.query.filter_by(orderID=self.order_id).first()
            if not order_model:
                self.error_message.append("没有该订单")
        if self.error_message:
            return False
        else:
            return True

    def write(self):
        """写入数据"""
        pro_model = PromotionModel.query.filter_by(search_id=self.search_id).first()  # 推广记录
        rate_id = pro_model.rate_id
        order_model = ParentOrderModel.query.filter_by(
            orderID=self.order_id).first() if self.order_status == "1" else None
        rate_model = RateModel.query.filter_by(name="已付款").first()  # 进度模型
        if not rate_model:  # 如果没有已付款的进度模型，创建一个
            rate_model = RateModel(name="已付款")
            pro_model.rate = rate_model
        elif rate_model.id > rate_id:  # 如果已付款的进度模型id大于推广记录的进度模型id，修改推广记录的进度模型
            pro_model.rate = rate_model
        pro_model.feeImgLink = self.save_path  # 保存路径
        pro_model.orderstatus = self.order_status  # 订单状态
        pro_model.order = order_model  # 订单
        db.session.add(pro_model)  # 添加到数据库
        db.session.commit()  # 提交到数据库
        return {"status": "success", "message": "修改成功"}


class writeNewPromotionModel(object):
    def __init__(self, form_dict):
        """传入的form_dict前端传入的数据，字典格式，包含了所有的数据"""
        """
        promotionPr                         ——>商品组，多选，列表，id
        promotionUser                       ——>联络人，id
        promotionRate                       ——>进度模型，id
        promotionFeeModel                   ——>费用模板，id
        promotionWechat                     ——>博主微信，str
        promotionCommission                 ——>佣金比例，float
        PromotionCheck                      ——>订单状态，str
        AccountList                         ——>推广账号列表，列表，字典，id，str
        promotionFee                        ——>费用，float    
        promotionCommission                 ——>佣金，float
        PromotionCheck                      ——>是否下单，str
        """
        self.form_dict = form_dict
        self.error_message = []
        self.pr = self.form_dict.get("promotionPr")
        self.user_id = self.form_dict.get("promotionUser")
        self.rate_id = self.form_dict.get("promotionRate")
        self.fee_model_id = self.form_dict.get("promotionFeeModel")
        self.wechat = self.form_dict.get("promotionWechat")

    def check(self):
        """检查数据是否正确"""
        group_model = GroupModel.query.filter(or_(GroupModel.id.in_(self.pr), GroupModel.name.in_(self.pr))).all()
        if not group_model:
            self.error_message.append("没有该商品组")  # 没有该商品组
        user_model = UserModel.query.filter_by(id=self.user_id).first()
        if not user_model:
            self.error_message.append("没有该联络人")  # 没有该联络人
        rate_model = RateModel.query.filter_by(id=self.rate_id).first()
        if not rate_model:
            self.error_message.append("没有该进度模型")  # 没有该进度模型
        fee_model = FeeModel.query.filter_by(id=self.fee_model_id).first()
        if not fee_model:
            self.error_message.append("没有该费用模板")  # 没有该费用模板
        bloger_model = BlogerModel.query.filter_by(wechat=self.wechat).first()
        if not bloger_model:
            bloger_model = BlogerModel(wechat=self.wechat)  # 没有该博主,创建博主
            db.session.add(bloger_model)
            db.session.commit()
        if self.error_message:
            return False
        else:
            return True

    def write(self, create_time=None):
        group_model = GroupModel.query.filter(
            or_(GroupModel.id.in_(self.pr), GroupModel.name.in_(self.pr))).all()  # 商品组
        bloger_model = BlogerModel.query.filter_by(wechat=self.wechat).first()  # 博主

        max_id = db.session.query(func.max(PromotionModel.id)).scalar() or 0  # 获取最大的id
        search_id = generate_Number_string(8, max_id + 1)  # 生成8位的id
        promotion_model = PromotionModel(search_id=search_id, fee=self.form_dict['promotionFee'],
                                         commission=self.form_dict['promotionCommission'],
                                         orderstatus=self.form_dict['PromotionCheck'],
                                         feeModel_id=self.fee_model_id, rate_id=self.rate_id, user_id=self.user_id,
                                         bloger=bloger_model)  # 创建推广模型
        promotion_model.group = group_model  # 商品组
        if create_time:
            promotion_model.createtime = create_time
        note_search_id = ""  # 生成推广内容的id
        for account_dict in self.form_dict['AccountList']:
            output_model = OutputModel.query.get(account_dict['outputModel'])  # 获取输出模型
            account_model = AccountModel.query.filter_by(account_id=account_dict['account']).first()  # 获取推广账号
            if not account_model:  # 如果没有该推广账号，就返回错误，提示先添加
                return {"status": "failed", "message": "数据库中没有该推广账号，请先添加"}
            account_model.bloger = bloger_model  # 将推广账号的博主设置为该博主
            max_id = db.session.query(func.max(PVContentModel.id)).scalar() or 0  # 获取最大的id
            note_search_id = generate_Number_string(8, max_id + 1)  # 生成8位的id
            new_PV_model = PVContentModel(account=account_model, output=output_model, search_id=note_search_id,
                                          promotion=promotion_model)  # 创建推广内容模型
            db.session.add(new_PV_model)  # 添加到数据库
        db.session.add(promotion_model)  # 添加到数据库
        db.session.commit()  # 提交
        return {"status": "success", "message": "新增成功", 'search_id': search_id, "note_search_id": note_search_id}


class WriteExcelPromotion(object):
    def __init__(self, save_path):
        """初始化"""
        """ header = 
        ["推广人", "博主微信", "账号主页链接", "平台", "推广产品，多个产品,隔开", "付费形式", "费用", "佣金", "图文链接", "产出形式","合作时间"]
        """
        print("初始化")
        self.save_path = save_path
        self.workbook = load_workbook(save_path)
        self.sheet = self.workbook.active
        self.data_list = []
        self.error_message = []
        self.Spam = ""

        self.account_dict = {}
        self.account_form = {}
        self.promotion_form = {}
        self.note_dict = {}

    def write(self):
        """写入文件"""
        i = 0
        print("真正开始写入")
        spydered_plat = ""
        for row in self.data_list:
            if self.Spam == "正常小红书账号已用完，请联系管理员":
                print("正常小红书账号已用完，请联系管理员")
                if row[3] == "小红书":
                    continue
            spyder_plat = row[3]
            if spyder_plat == spydered_plat:  # 如果平台不同，则创建新账号
                if spyder_plat == "小红书":
                    time.sleep(random.randint(2, 13))
                else:
                    time.sleep(random.randint(2, 5))
            account_result = self.writeAccount(row)  # 写入账号
            if account_result:  # 如果账号写入成功，则创建新推广，并将账号信息添加到推广中
                self.writePromotion(row)  # 写入推广
                time.sleep(random.randint(2, 13)) if spyder_plat == "小红书" else time.sleep(random.randint(2, 5))
                self.writrNote(row)  # 写入推广内容
                spydered_plat = row[3]

            print(f'共计：{len(self.data_list)}行数据,目前已经进行至{i}行')
            print(row)
            print(self.error_message)
            i += 1

    def readPromotionExcel(self):  # 读取推广表格
        workbook = load_workbook(self.save_path)  # 打开excel文件
        sheet = workbook.active  # 获取当前活跃的sheet,默认是第一个sheet
        self.total = 0
        for row in sheet.rows:  # 逐行读取
            if row[0].row == 1:  # 跳过第一行
                continue
            row_list = [cell.value for cell in row]  # 读取每行的数据
            self.data_list.append(row_list)  # 读取每行的数据
            self.total += 1

    def check(self):
        """检查数据"""
        new_data_list = []
        print("开始检查数据")
        self.checked = 1  # 因为已经跳过第一行，所以计数从2开始
        for row in self.data_list:
            if PlatModel.query.filter_by(name=row[3]).first() is None:  # 检查平台是否存在
                self.error_message.append(f"第{self.checked}行的平台不存在")
                continue
            if OutputModel.query.filter_by(name=row[9]).first() is None:  # 检查产出形式是否存在
                self.error_message.append(f"第{self.checked}行的输出模板不存在")
                continue
            if GroupModel.query.filter_by(name=row[4]).first() is None:  # 检查商品组是否存在
                self.error_message.append(f"第{self.checked}行的商品组不存在")
                continue
            if UserModel.query.filter_by(name=row[0]).first() is None:  # 检查推广人是否存在
                self.error_message.append(f"第{self.checked}行的联络人不存在")
                continue
            if FeeModel.query.filter_by(name=row[5]).first() is None:  # 检查费用模型是否存在
                self.error_message.append(f"第{self.checked}行的费用模板不存在")
                continue
            if row[8]:
                content_link = row[8].split("?")[0] if row[3] == "小红书" else row[8]
                if PVContentModel.query.filter_by(content_link=content_link).first() is not None:
                    continue
            new_data_list.append(row)  # 将检查通过的数据添加到新列表中

            print("通过检查：{}/{}".format(self.checked, self.total))
            self.checked += 1
        self.data_list = new_data_list  # 将检查通过的数据赋值给原来的列表

    def writeAccount(self, row):
        self.account_form['platId'] = PlatModel.query.filter_by(name=row[3]).first().id  # 获取平台id
        self.account_form['profileLink'] = row[2]  # 获取账号主页链接
        account = searchAccount(self.account_form)  # 搜索账号
        if account.check():
            print("通过初次检查，检查账号是否存在")
            if not account.checkExist():  # 检查账号是否存在，不存在则继续爬取并且写入数据库
                print("账号不存在，开始爬取")
                account_info = account.sypderAccount()  # 爬取账号
                if account_info['status'] == "success":  # 检查爬取是否成功
                    print("爬取成功，开始写入数据库")
                    account_info = account.writeAccount()  # 写入数据库
                    self.account_dict["account"] = account_info['message']['account_id']
                    return True
                elif account_info['status'] == "2":
                    print("触发反爬虫，回弹重试")
                    return self.writeAccount(row)
                else:
                    print(account_info['message'])
                    print("爬取账号失败")
                    self.Spam = account_info['message']
                    return False
            else:  # 如果账号存在，则获取账号id
                print("账号已经存在，不需要爬取")
                self.account_dict["account"] = AccountModel.query.filter_by(
                    profile_link=row[2]).first().account_id  # 获取账号id
                return True
        else:
            print("账号不存在，返回False")
            return False

    def writePromotion(self, row):
        self.account_dict['outputModel'] = OutputModel.query.filter_by(name=row[9]).first().id  # 获取产出形式id
        self.promotion_form['promotionPr'] = row[4].split(",")  # 获取推广产品
        self.promotion_form['promotionUser'] = UserModel.query.filter_by(name=row[0]).first().id  # 获取推广人id
        self.promotion_form['promotionRate'] = RateModel.query.filter_by(name="已约稿").first().id  # 获取进度模型id
        self.promotion_form['promotionFeeModel'] = FeeModel.query.filter_by(name=row[5]).first().id  # 获取费用模型id
        self.promotion_form['promotionFee'] = row[6]  # 获取费用
        self.promotion_form['promotionCommission'] = row[7]  # 获取佣金
        self.promotion_form['promotionWechat'] = row[1]  # 获取微信号
        self.promotion_form['PromotionCheck'] = "0"  # 获取是否拍单
        self.promotion_form['AccountList'] = [self.account_dict]  # 获取账号列表
        create_time = row[10]  # 获取创建时间
        write = writeNewPromotionModel(self.promotion_form)  # 初始化写入推广模型
        if write.check():  # 检查数据
            print("数据检查通过，开始写入推广")
            self.new_promotion_result = write.write(create_time=create_time)  # 写入推广，返回写入结果
            if self.new_promotion_result['status'] == "failed":  # 检查写入是否成功，如果失败则返回错误信息
                print("写入失败，返回错误信息")
                self.error_message.append(f"{self.account_form['profileLink']}:{self.new_promotion_result['message']}")
                return False
            else:
                print("写入成功")
                return True
        else:
            print("推广写入数据检查失败，返回错误信息")
            print(write.error_message)
            return False

    def writrNote(self, row):

        promotion_id = PromotionModel.query.filter_by(
            search_id=self.new_promotion_result['search_id']).first().id  # 获取推广id
        self.note_dict['promotion_id'] = promotion_id  # 获取推广id
        self.note_dict['account_id'] = self.account_dict['account']  # 获取账号id
        self.note_dict['note_id'] = self.new_promotion_result['note_search_id']  # 获取笔记id
        self.note_dict['noteLink'] = row[8]  # 获取笔记链接
        create_time = row[10]  # 获取创建时间

        search_note = searchNotes(self.note_dict)
        if search_note.check():
            note_info = search_note.spyderNote()
            print(note_info)
            if note_info['status'] == "success":
                search_note.writeNote(create_time=create_time)
                print("笔记写入成功")
                return True
            elif note_info["status"] == "1":
                print("笔记状态出错，更新笔记时间")
                note_model = PVContentModel.query.filter_by(search_id=self.note_dict['note_id']).first()
                note_model.create_time = create_time
                db.session.add(note_model)
                db.session.commit()
                return True
            elif note_info["status"] == "2":
                return self.writrNote(row)
            elif note_info["status"] == "failed":
                print(note_info['message'])

                self.Spam = note_info['message']
                return False
        else:
            print("笔记检查失败，返回错误信息")
            return False
