import hashlib
import math
import time
import random
from datetime import datetime

from flask_mail import Message

from APP.SQLAPP.addEdit.dataWrite import writeLocationModel
from APP.SQLAPP.addEdit.orderStore import writeRefund, writeOrderData, WriteExcelOrder
from APP.SQLAPP.addEdit.promotion import WriteExcelPromotion, WriteSQLData
from APP.SQLAPP.search.promotion import searchNotes, searchPVContentSql2
from APP.Spyder.KdzsSpyder import KuaiDiZhuShouSpyder
from exts import mail
from celery import Celery

from models.promotiondata import PVContentModel, PVDataModel

kdzs = KuaiDiZhuShouSpyder()


def send_mail(recipient, subject, body):
    message = Message(subject=subject, recipients=[recipient], body=body)
    mail.send(message=message)
    print("发送成功")


def GetAddress():
    writeLocationModel()
    print("发送成功")


def GetXHSNote(self, plat):
    contents = searchPVContentSql2(self=self, plat=plat)
    i = 1
    for content in contents:
        note_link = content.link
        date_today = datetime.now().strftime("%Y-%m-%d")
        info = note_link + date_today
        DaydataID = hashlib.sha1(info.encode()).hexdigest()[:20]
        pvcontent_today_model = PVDataModel.query.filter(PVDataModel.search_id == DaydataID).first()
        if pvcontent_today_model:
            if pvcontent_today_model.liked:
                i += 1
                print("共计{}条小红书待更新，已更新至第{}条,剩余{}条".format(len(contents), i, len(contents) - i))
                continue
        token_status = GetXHSNote2(note_link)
        if token_status == "4":
            print("token已经全部失效")
            break
        elif token_status == "0":
            print("链接错误")
            continue
        i += 1
        print("共计{}条小红书待更新，已更新至第{}条,剩余{}条".format(len(contents), i, len(contents) - i))
        time.sleep(random.randint(30, 50))


def GetXHSNote2(note_link):
    notes = searchNotes()
    result = notes.spyderXHSNote(note_link=note_link)
    write = WriteSQLData()
    print(note_link)
    if result['status'] == "1":
        # 等于1时返回了正确数据，写入到数据库
        write.WriteSqlPVcontentData(note_link, result['message'])
        return "1"
    elif result['status'] == "2":
        # 等于2时是token过期，重新获取token，然后重新爬取
        if result['message'] == "token过期" or result['message'] == "登录已过期":
            token_status = notes.spyderXHSNote(note_link=note_link)
            return token_status
        else:
            write.changeSQLNoteStatus(note_link, result['message'])
            return "1"
    elif result['status'] == "3":
        write.changeSQLNoteStatus(note_link, result['message'])
    elif result['status'] == "4":
        # 全部token失效
        return "4"
    elif result['status'] == "0":
        # 链接错误
        return "0"


def GetDYNote(self, plat):
    contents = searchPVContentSql2(self=self, plat=plat)
    i = 1
    for content in contents:
        note_link = content.link
        date_today = datetime.now().strftime("%Y-%m-%d")
        info = note_link + date_today
        DaydataID = hashlib.sha1(info.encode()).hexdigest()[:20]
        pvcontent_today_model = PVDataModel.query.filter(PVDataModel.search_id == DaydataID).first()
        if pvcontent_today_model:
            if pvcontent_today_model.liked:
                i += 1
                print("共计{}条抖音待更新，已更新至第{}条,剩余{}条".format(len(contents), i, len(contents) - i))
                continue
        token_status = GetDYNote2(note_link)
        if token_status == "4":
            print("token已经全部失效")
            break
        elif token_status == "0":
            i += 1
            print("链接错误")
            print("共计{}条抖音待更新，已更新至第{}条,剩余{}条".format(len(contents), i, len(contents) - i))
            continue
        i += 1
        print("共计{}条抖音待更新，已更新至第{}条,剩余{}条".format(len(contents), i, len(contents) - i))
        time.sleep(random.randint(5, 8))


def GetDYNote2(note_link):
    notes = searchNotes()
    result = notes.spyderDYNote(note_link=note_link)
    print(note_link)
    write = WriteSQLData()
    if result['status'] == "1":
        # 等于1时返回了正确数据，写入到数据库
        write.WriteSqlPVcontentData(note_link, result['message'])
        return "1"

    elif result['status'] == "2":
        # 等于2时是token过期，重新获取token，然后重新爬取
        if result['message'] == "token过期" or result['message'] == "登录已过期":
            token_status = notes.spyderXHSNote(note_link=note_link)
            return token_status
        else:
            write.changeSQLNoteStatus(note_link, result['message'])
            return "1"
    elif result['status'] == "3":
        write.changeSQLNoteStatus(note_link, result['message'])
        return "1"
    elif result['status'] == "4":
        # 全部token失效
        return "4"
    elif result['status'] == "0":
        # 链接错误
        return "0"


def GetOrders(stores, endDate, startDate, token):
    order_JSON = kdzs.getOrder(stores, endDate=endDate, startDate=startDate, token=token)
    totalCount = order_JSON['total']
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
        order_JSON = kdzs.getOrder(pageNo=page, stores=stores, endDate=endDate, startDate=startDate, token=token)
        dealResults = kdzs.DealOrder(order_JSON=order_JSON)
        for dealresult in dealResults:
            print(i)
            writeOrderData(dealresult)
            status["processed"] = i
            i += 1
        time.sleep(80)
    return status


def writeHandOrder(save_path):
    write = WriteExcelOrder(save_path)
    dealResults = write.dealHandOrder()
    for dealresult in dealResults:
        print(dealresult)
        writeOrderData(dealresult)


def GetRefund(endDate, startDate, token):
    refund_json = kdzs.getRefund(endDate=endDate, startDate=startDate, token=token)
    pageCount = refund_json['total']
    pageNo = math.ceil(int(pageCount) / 200)
    refund_order = kdzs.dealRefund(refund_json)
    i = 0
    status = {"total": pageCount, "processed": 0}
    for refund in refund_order:
        writeRefund(refund)
        i += 1
        status["processed"] = i
    for page in range(2, pageNo + 1):
        refund_json = kdzs.getRefund(endDate=endDate, startDate=startDate, pageNo=page, token=token)
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
    write = WriteExcelPromotion(save_path)
    write.readPromotionExcel()
    write.check()
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
    celery.task(name="GetXHSNote")(GetXHSNote)
    celery.task(name="GetDYNote")(GetDYNote)
    celery.task(name="GetAddress")(GetAddress)
    celery.task(name="writeFilePromotionC")(writeFilePromotionC)
    celery.task(name="writeHandOrder")(writeHandOrder)

    return celery
