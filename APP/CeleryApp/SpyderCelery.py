import hashlib
import random
import time
from datetime import datetime

from APP.SQLAPP.addEdit.promotion import WriteSQLData
from APP.SQLAPP.search.promotion import searchAccountNotes, searchAccountSql2, searchAccount, searchNotes, \
    searchPVContentSql2
from APP.Spyder.makeRealURL import MakeRealURL
from exts import db
from models.promotion import AccountDayDataModel
from models.promotiondata import PVDataModel


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


def getNote(attention, plat):
    notes = searchNotes()
    contents = searchPVContentSql2(attention=attention, plat=plat)
    i = 1
    for content in contents:
        url = content.link
        DaydataID = MakeRealURL().makeUniqueDayId(url)
        pvcontent_today_model = PVDataModel.query.filter(PVDataModel.search_id == DaydataID).first()
        if pvcontent_today_model:
            i += 1
            print("共计{}条{}图文数据待更新，已更新至第{}条,剩余{}条".format(len(contents) + 1, plat, i,
                                                                            len(contents) + 1 - i))
            continue
        if plat == "小红书":
            result = notes.spyderXHSNote(note_link=url)
        elif plat == "抖音":
            result = notes.spyderDYNote(note_link=url)
        else:
            continue
        status = writeNote(result, url)
        if status == "4":
            print("token已经全部失效")
            break
        elif status == "0":
            print("链接错误")
            continue
        i += 1
        print("共计{}条{}图文数据待更新，已更新至第{}条,剩余{}条".format(len(contents) + 1, plat, i,
                                                                        len(contents) + 1 - i))
        if len(contents) + 1 - i == 0:
            break
        time_plat_sleep(plat)


def writeNote(result, note_link):
    write = WriteSQLData()
    if result['status'] == "1":
        # 等于1时返回了正确数据，写入到数据库
        write.WriteSqlPVcontentData(note_link, result['message'], )
        return "1"
    elif result['status'] == "2":
        # 等于2时是token过期，重新获取token，然后重新爬取
        write.changeSQLNoteStatus(note_link, result['message'])
    elif result['status'] == "3":
        write.changeSQLNoteStatus(note_link, result['message'])
    elif result['status'] == "4":
        # 全部token失效
        return "4"
    elif result['status'] == "0":
        # 链接错误
        return "0"


def getAccount(attention, plat):
    contents = searchAccountSql2(attention=attention, plat=plat)
    accounts = searchAccount()
    i = 1
    for content in contents:
        link = content.link
        DaydataID = makeHASID(link)
        account_today_model = AccountDayDataModel.query.filter(AccountDayDataModel.search_id == DaydataID).first()
        if account_today_model:
            i += 1
            print("共计{}条{}图文数据待更新，已更新至第{}条,剩余{}条".format(len(contents) + 1, plat, i,
                                                                            len(contents) + 1 - i))
            continue
        if plat == "小红书":
            result = accounts.sypderXHSAccount(profile_link=link)
        elif plat == "抖音":
            result = accounts.spyderDYAccount(profile_link=link)
        else:
            return "0"
        status = writeAccount(link, result, plat)
        if status == "4":
            print("token已经全部失效")
            break
        elif status == "0":
            print("链接错误")
            continue
        i += 1
        print("共计{}条{}图文数据待更新，已更新至第{}条,剩余{}条".format(len(contents) + 1, plat, i,
                                                                        len(contents) + 1 - i))
        if len(contents) + 1 - i == 0:
            break
        time_plat_sleep(plat)


def writeAccount(profile_link, result, plat):
    write = WriteSQLData()
    if result['status'] == "1":
        # 等于1时返回了正确数据，写入到数据库
        write.WriteSqlAccount(profile_link, result['message'], plat=plat)
    elif result['status'] == "2":
        write.changeSQLAccountStatus(profile_link, result['message'])
    elif result['status'] == "3":
        write.changeSQLAccountStatus(profile_link, result['message'])
    elif result['status'] == "4":
        # 全部token失效
        return "4"
    elif result['status'] == "0":
        # 链接错误
        return "0"


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


def getDYAccountNote(profile_link, account_Info):
    max_cursor = "0"
    i = 0
    notes = int(account_Info.get("notes")) if account_Info.get("notes") else 0
    Continue = True
    while Continue:
        token_status = GetDYAccountNote2(profile_link=profile_link, max_cursor=max_cursor)
        for tokens in token_status:
            i += 1
            print("共计{}条抖音待更新，已更新至第{}条,剩余{}条".format(notes, i, notes - i))
            token, has_more, max_cursor = tokens
            if token_status == "4":
                print("token已经全部失效")
                break
            if not has_more:
                Continue = False
                break
        time_plat_sleep("抖音")


def GetDYAccountNote2(profile_link, max_cursor):
    notes = searchAccountNotes()
    results = notes.spyderDYAccountNote(profile_link=profile_link, max_cursor=max_cursor)
    write = WriteSQLData()
    for result in results:
        max_cursor = result.get("max_cursor")
        has_more = result.get("has_more")
        if result['status'] == "1":
            # 等于1时返回了正确数据，写入到数据库
            write.writeAccountNotes(profile_link, result['message'])
            yield "1", has_more, max_cursor
        elif result['status'] == "2":
            # 等于2时是token过期，重新获取token，然后重新爬取
            if result['message'] == "token过期" or result['message'] == "登录已过期":
                yield GetDYAccountNote2(profile_link=profile_link, max_cursor=max_cursor)
            else:
                write.changeSQLNoteStatus(profile_link, result['message'])
                yield "2", has_more, max_cursor
        elif result['status'] == "3":
            write.changeSQLNoteStatus(profile_link, result['message'])
            yield "3", has_more, max_cursor
        elif result['status'] == "4":
            # 全部token失效
            yield "4", has_more, max_cursor
