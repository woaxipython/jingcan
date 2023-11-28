import hashlib
import math
import time
import random
from datetime import datetime

from flask_mail import Message

from APP.CeleryApp.OrderCelery import getOrder
from APP.CeleryApp.SpyderCelery import getAccount, getNote, getDYAccountNote
from APP.SQLAPP.addEdit.dataWrite import writeLocationModel
from APP.SQLAPP.addEdit.orderStore import writeRefund, writeOrderData, WriteExcelOrder
from APP.SQLAPP.addEdit.promotion import WriteSQLData, WriteExcelPVContent
from APP.SQLAPP.search.promotion import searchAccountNotes
from APP.Spyder.KdzsSpyder import KuaiDiZhuShouSpyder
from exts import mail, db
from celery import Celery

from models.back import PlatModel
from models.promotion import AccountModel, AccountDayDataModel
from models.promotiondata import PVContentModel, PVDataModel

kdzs = KuaiDiZhuShouSpyder()


def send_mail(recipient, subject, body):
    message = Message(subject=subject, recipients=[recipient], body=body)
    mail.send(message=message)
    print("发送成功")


def GetAddress():
    writeLocationModel()
    print("发送成功")


def makeHASID(link):
    date_today = datetime.now().strftime("%Y-%m-%d")
    info = link + date_today
    hasID = hashlib.sha1(info.encode()).hexdigest()[:20]
    return hasID


def time_plat_sleep(plat):
    if plat == "小红书":
        time.sleep(random.randint(15, 30))
    elif plat == "抖音":
        time.sleep(random.randint(3, 8))


def GetAccount(attention, plat):
    getAccount(attention=attention, plat=plat)


def GetNote(attention, plat):
    # changePlat()
    getNote(attention=attention, plat=plat)


def GetAccountNote(profile_link, account_Info, plat):
    if plat == "小红书":
        getXHSAccountNote(profile_link=profile_link, account_Info=account_Info)
    elif plat == "抖音":
        getDYAccountNote(profile_link=profile_link, account_Info=account_Info)


def getXHSAccountNote(profile_link, account_Info):
    notes = int(account_Info.get("notes")) if account_Info.get("notes") else 0
    pages = notes // 6 + 1
    i = 1
    for page in range(1, pages + 1):
        token_status = GetXHSAccountNote2(profile_link=profile_link, page=page)
        if token_status == "4":
            print("token已经全部失效")
            break
        i += 6
        print("共计{}条小红书待更新，已更新至第{}条,剩余{}条".format(notes, i, notes - i))
        time_plat_sleep("小红书")


def GetXHSAccountNote2(profile_link, page):
    notes = searchAccountNotes()
    results = notes.spyderXHSAccountNote(profile_link=profile_link, page=page)
    write = WriteSQLData()
    for result in results:
        if result['status'] == "1":
            # 等于1时返回了正确数据，写入到数据库
            write.writeAccountNotes(profile_link, result['message'])
        elif result['status'] == "2":
            # 等于2时是token过期，重新获取token，然后重新爬取
            if result['message'] == "token过期" or result['message'] == "登录已过期":
                return GetXHSAccountNote2(profile_link=profile_link, page=page)
            else:
                write.changeSQLNoteStatus(profile_link, result['message'])
        elif result['status'] == "3":
            write.changeSQLNoteStatus(profile_link, result['message'])
        elif result['status'] == "4":
            # 全部token失效
            return "4"


def GetOrders(stores, endDate, startDate, token):
    getOrder(stores=stores, endDate=endDate, startDate=startDate, token=token)


def writeHandOrder(save_path):
    write = WriteExcelOrder(save_path)
    dealResults = write.dealHandOrder()
    totalCount = len(dealResults)
    i = 1
    for dealresult in dealResults:
        print(dealresult)
        writeOrderData(dealresult)
        print("共计{}条订单，已更新至第{}条,剩余{}条".format(totalCount, i, totalCount - i))


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


def writeFilePVContent(save_path):
    write = WriteExcelPVContent(save_path)
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
    celery.task(name="GetAddress")(GetAddress)
    celery.task(name="writeFilePVContent")(writeFilePVContent)
    celery.task(name="writeHandOrder")(writeHandOrder)

    celery.task(name="GetNote")(GetNote)
    celery.task(name="GetAccount")(GetAccount)
    celery.task(name="GetAccountNote")(GetAccountNote)

    return celery
