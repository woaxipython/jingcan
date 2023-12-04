# -*- coding: utf-8 -*-

import pandas as pd


def PromotionData(sql_list, cycle=""):
    columns = ["date", "group_name", "bloger", "user", "fee", "output", "rate", "plat", "account", "title", "status",
               "content_link", "liked", "collected", "commented"]
    pro = pd.DataFrame(sql_list, columns=columns)
    pro["liked"] = pro["liked"].fillna(0)
    pro["collected"] = pro["collected"].fillna(0)
    pro["commented"] = pro["commented"].fillna(0)
    pro["fee"] = pro["fee"].fillna(0)
    pro["title"] = pro["title"].fillna("None")
    pro["content_link"] = pro["content_link"].fillna("")
    pro['account'] = pro['account'].fillna("None")
    pro = pro.sort_values(by='date', ascending=True)
    pro = pro.reset_index()
    pro['date'] = pd.to_datetime(pro['date'])
    pro = pro.set_index('date')

    wait_send_data = waitSend(pro)
    un_normal_data = unNormal(pro)
    bloger_data = mainBlogerData(pro)
    pv_data_list = mainPvcontentData(pro)

    have_send = int(pro[pro["content_link"] != ""].count()["content_link"])
    wait_send = int(pro['content_link'].count() - have_send)
    normal = int(pro[pro["status"] == "正常"].count()["status"])
    un_normal = int(pro['status'].count() - normal)
    account = len(pro["account"].unique().tolist())
    pvcontent = len(pro["content_link"].unique().tolist())

    pvcontent_l = len(pv_data_list)

    return [have_send, wait_send, normal, un_normal, account, 10, pvcontent, pvcontent_l, wait_send_data,
            un_normal_data, bloger_data, pv_data_list]


def makePVEcel(sql_list, save_path):
    columns = ['上传日期', '产品', '账号', '账号链接', '是否自营', '标题', '数据库ID', '图文链接', '点赞量', '评论量',
               '转发量', '收藏量', '视频链接(小红书无效)', '图文链接', '内容形式', '重点关注', '平台']
    pro = pd.DataFrame(sql_list, columns=columns)
    pro.to_excel(save_path, index=False)


def mainPvcontentData(pro):
    pv_data = pro.drop_duplicates(subset=['title'], keep='first')
    pv_data = pv_data.reset_index()
    pv_data = pv_data.sort_values(by='date', ascending=True)
    pv_data = pv_data[
        ["bloger", "plat", "account", "status", "fee", "date", "user", "group_name", "output", "rate", "title",
         "content_link", "liked", "collected", "commented", ]]
    pv_data['date'] = pv_data['date'].dt.strftime('%Y-%m-%d')

    pv_data = pv_data.sort_values(by='liked', ascending=False)
    pv_data = pv_data.reset_index()
    pv_data = pv_data[pv_data['liked'] > 800]
    pv_data = pv_data.drop(['index'], axis=1)
    return pv_data.values.tolist()


def mainBlogerData(pro):
    bloger_data = pro.groupby('bloger', ).agg({'liked': 'sum', 'collected': 'sum', 'commented': 'sum', 'user': 'first'})

    bloger_data = bloger_data.sort_values(by='liked', ascending=False)
    bloger_data = bloger_data.reset_index()

    bloger_data = bloger_data.sort_values(by='liked', ascending=False)
    bloger_data = bloger_data.reset_index()
    bloger_data = bloger_data[["bloger", "liked", "collected", "commented", "user"]]
    bloger_data = bloger_data[:10]
    bloger_data = bloger_data
    return bloger_data.values.tolist()


def waitSend(pro):
    wait_send_data = pro[pro["content_link"] == ""]
    wait_send_data = wait_send_data.reset_index()
    wait_send_data = wait_send_data.sort_values(by='date', ascending=True)
    wait_send_data = wait_send_data[
        ["bloger", "plat", "account", "status", "fee", "date", "user", "group_name", "output", "rate"]]
    wait_send_data['date'] = wait_send_data['date'].dt.strftime('%Y-%m-%d')
    # wait_send_data['account'] = "1"
    return wait_send_data.values.tolist()


def unNormal(pro):
    un_normal_data = pro[pro["status"] != "正常"]
    un_normal_data = un_normal_data.reset_index()
    un_normal_data = un_normal_data.sort_values(by='date', ascending=True)
    un_normal_data = un_normal_data[
        ["bloger", "plat", "account", "status", "fee", "date", "user", "group_name", "output", "rate", "title",
         "content_link", "liked", "collected", "commented", ]]
    un_normal_data['date'] = un_normal_data['date'].dt.strftime('%Y-%m-%d')
    # un_normal_data['title'] = "1"
    # un_normal_data['account'] = "1"
    return un_normal_data.values.tolist()


def promotionChartData(sql_list, cycle="D", values="count"):
    columns = ["date", "plat", "count", "liked", "commented", "collected"]
    pro = pd.DataFrame(sql_list, columns=columns)
    pro["liked"] = pro["liked"].fillna(0)
    pro["collected"] = pro["collected"].fillna(0)
    pro["commented"] = pro["commented"].fillna(0)
    pro["count"] = pro["count"].fillna(0)
    pro['date'] = pd.to_datetime(pro['date'])
    pro = pro.pivot_table(index=pd.Grouper(key="date", freq=cycle), columns=["plat"], values=values,
                          aggfunc='sum').fillna(0)
    pro = pro.reset_index()
    pro['date'] = pro['date'].dt.strftime('%Y-%m-%d')
    pro = pro.to_dict(orient="list")

    data_dict = {}
    for key, value in pro.items():
        new_pro = {}
        if key[0] == "date":
            new_pro[key[0]] = value
        else:
            new_pro[key[1]] = value
        if data_dict.get(key[0]):
            data_dict[key[0]].update(new_pro)
        else:
            data_dict[key[0]] = new_pro if key[0] != "date" else value
    return data_dict
