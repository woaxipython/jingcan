import math
import time
import random

from flask_mail import Message

from APP.SQLAPP.addEdit.dataWrite import writeLocationModel
from APP.SQLAPP.addEdit.orderStore import writeRefund, writeOrderData
from APP.SQLAPP.addEdit.promotion import WriteExcelPromotion
from APP.SQLAPP.search.promotion import RefreshData, searchNotes
from APP.Spyder.KdzsSpyder import KuaiDiZhuShouSpyder
from exts import mail
from celery import Celery

from models.promotiondata import PVContentModel

kdzs = KuaiDiZhuShouSpyder()


def send_mail(recipient, subject, body):
    message = Message(subject=subject, recipients=[recipient], body=body)
    mail.send(message=message)
    print("发送成功")


def GetAddress():
    writeLocationModel()
    print("发送成功")


def refreshPromotion():
    content_list = PVContentModel.query.all()
    totalCount = len(content_list)
    i = 0
    h = 0
    status = {"total": totalCount, "processed": i, "failed": h}
    Spam = ""
    spydered_plat = ""
    for content in content_list:
        refresh_data = RefreshData(content)
        if refresh_data.check():
            print(content.title, "开始更新")
            if Spam == "正常小红书账号已用完，请联系管理员":
                print("正常小红书账号已用完，请联系管理员")
                if content.plat.name == "小红书":
                    continue
            spyder_plat = content.account.plat.name
            if spyder_plat == spydered_plat:  # 如果是同一个平台，就休息一下
                time.sleep(random.randint(2, 30)) if spyder_plat == "小红书" else time.sleep(random.randint(2, 5))

            note_dict = refresh_data.makeData()
            search_note = searchNotes(note_dict)
            if search_note.check():
                note_info = search_note.spyderNote()
                spydered_plat = content.account.plat.name
                if note_info['status'] == "success":
                    write_result = refresh_data.writeData(search_note.profile_result)
                    i += 1
                    status["processed"] = i
                    print(search_note.profile_result['title'])
                    print(write_result)
                elif note_info["status"] == "1":
                    notes_Info = {
                        "liked": 0,
                        "collected": 0,
                        "commented": 0,
                        "forwarded": 0
                    }
                    refresh_data.writeData(notes_Info)
                    i += 1
                    status["processed"] = i
                    print("录入异常数据")
                elif note_info["status"] == "2":
                    print("正常小红书账号已用完，请联系管理员")
                    Spam = "正常小红书账号已用完，请联系管理员"
                    continue
            else:
                print(search_note.error_message)
                continue
        else:
            h += 1
            print(content.title, "已更新")
            continue
        status["processed"] = i
        print(status)
        print("............................................")
    return status


def GetOrders(stores, endDate, startDate):
    order_JSON = kdzs.getOrder(stores, endDate=endDate, startDate=startDate)
    totalCount = order_JSON['total']
    print(totalCount)
    pageNo = math.ceil(int(totalCount) / 1000)
    dealResults = kdzs.DealOrder(order_JSON=order_JSON)
    i = 1
    status = {"total": totalCount, "processed": 0}
    for dealresult in dealResults:
        writeOrderData(dealresult)
        i += 1
        status["processed"] = i
        print(i)
    for page in range(2, pageNo + 1):
        order_JSON = kdzs.getOrder(pageNo=page, stores=stores, endDate=endDate, startDate=startDate)
        dealResults = kdzs.DealOrder(order_JSON=order_JSON)
        for dealresult in dealResults:
            print(i)
            writeOrderData(dealresult)
            status["processed"] = i
            i += 1
        time.sleep(80)
    return status


def GetRefund(endDate, startDate):
    refund_json = kdzs.getRefund(endDate=endDate, startDate=startDate)
    pageCount = refund_json['total']
    print(pageCount)
    pageNo = math.ceil(int(pageCount) / 200)
    refund_order = kdzs.dealRefund(refund_json)
    i = 0
    status = {"total": pageCount, "processed": 0}
    for refund in refund_order:
        writeRefund(refund)
        i += 1
        status["processed"] = i
    for page in range(2, pageNo + 1):
        refund_json = kdzs.getRefund(endDate=endDate, startDate=startDate, pageNo=page)
        refund_order = kdzs.dealRefund(refund_json)
        for refund in refund_order:
            writeRefund(refund)
            print(i)
            i += 1
            status["processed"] = i
        time.sleep(80)
    return status


"""根据celery重构了celery任务"""


def writeFilePromotionC(save_path):
    print("开始写入")
    write = WriteExcelPromotion(save_path)
    write.readPromotionExcel()
    write.check()
    print(write.error_message)
    write.write()


# 创建Celery对象
def make_celery(app):
    celery = Celery(app.import_name, backend=app.config["CELERY_RESULT_BACKEND"],
                    broker=app.config['CELERY_BROKER_URL'])
    TaskBase = celery.Task

    class ContexTask(TaskBase):
        abstract = True

        def __call__(self, *args, **kwargs):
            # app.app_context会自动创建一个临时的app返回，是可以直接调用的,使用current_app调用
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)

    celery.Task = ContexTask
    app.celery = celery
    # 添加任务
    celery.task(name="send_mail")(send_mail)
    celery.task(name="GetOrders")(GetOrders)
    celery.task(name="GetRefund")(GetRefund)
    celery.task(name="refreshPromotion")(refreshPromotion)
    celery.task(name="GetAddress")(GetAddress)
    celery.task(name="writeFilePromotionC")(writeFilePromotionC)

    return celery
