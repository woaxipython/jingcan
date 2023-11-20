from datetime import timedelta

from flask import Blueprint, request, current_app, render_template, session, send_file, \
    jsonify
from werkzeug.utils import secure_filename

from APP.SQLAPP.makePandas.promotion import promotionChartData, promotionChartData2
from APP.SQLAPP.search.promotion import GetPromotionModel

bp = Blueprint("pro", __name__, url_prefix="/pro")


@bp.route("/data")
def data():
    return render_template("html/promotion/promotionData.html")


@bp.route("/chartData")
def chartData():
    cycle = request.args.get("cycle")
    promotions = GetPromotionModel(interval=9000)
    promotions = promotions.getSQlData()
    plat_count = promotionChartData(promotions, cycle="W", values='output', column="plat", count=True)
    plat_count = plat_count.reset_index()
    plat_count['date'] = plat_count['date'].dt.strftime('%Y-%m-%d')
    message = {"plat": {}, "plat_liked": {}, "collected": {}, "commented": {}}
    for col in plat_count.columns:
        message["plat"][col] = plat_count[col].T.values.tolist()

    plat_sum = promotionChartData(promotions, cycle="W", values=["liked", "collected", "commented", ], column="plat",
                                  count=False)
    plat_sum = plat_sum.reset_index()
    plat_sum['date'] = plat_sum['date'].dt.strftime('%Y-%m-%d')

    plat_liked = plat_sum['liked'].copy()
    plat_liked.insert(0, "date", plat_sum['date'])
    for col in plat_liked.columns:
        message["plat_liked"][col] = plat_liked[col].T.values.tolist()

    plat_collected = plat_sum['collected'].copy()
    plat_collected.insert(0, "date", plat_sum['date'])
    for col in plat_collected.columns:
        message["collected"][col] = plat_collected[col].T.values.tolist()

    plat_commented = plat_sum['commented'].copy()
    plat_commented.insert(0, "date", plat_sum['date'])
    for col in plat_commented.columns:
        message["commented"][col] = plat_commented[col].T.values.tolist()

    return jsonify(message)


@bp.route("/chartData2")
def chartData2():
    promotions = GetPromotionModel(interval=9000)
    promotions = promotions.getSQlData()
    user_count = promotionChartData(promotions, cycle="M", values=["fee"], column=["user", "content_link"],
                                    count=True)
    user_count = user_count.reset_index()
    columns = []
    for column in user_count.columns:
        columns.append("-".join([x for x in column if x != "" and x != "fee"]))
    user_count.columns = columns
    name_list = []
    status_list = []
    for column in columns:
        if column == "date":
            continue
        name, status = column.split("-")
        name_list.append(name)
        status_list.append(status)
    i = len(name_list) - 1
    while i >= 0:
        print(i, len(name_list))
        if i == len(name_list) - 1:
            name_z = name_list[i]
            name_b = name_list[i - 1]
            status_f = status_list[i]
            if name_z != name_b:
                new_name = name_z + "-" + "已发稿" if status_f == "未发稿" else name_z + "-" + "未发稿"
                user_count[new_name] = 0
                print(name_z, name_b, status_f, new_name)
        elif i != 0:
            name_f = name_list[i + 1]
            name_z = name_list[i]
            name_b = name_list[i - 1]
            status_f = status_list[i]
            if name_z != name_f and name_z != name_b:
                new_name = name_z + "-" + "已发稿" if status_f == "未发稿" else name_z + "-" + "未发稿"
                user_count[new_name] = 0
                print(name_z, name_f, name_b, status_f, new_name)
        else:
            name_f = name_list[i + 1]
            name_z = name_list[i]
            status_f = status_list[i]
            if name_z != name_f:
                new_name = name_z + "-" + "已发稿" if status_f == "未发稿" else name_z + "-" + "未发稿"
                user_count[new_name] = 0
                print(name_z, name_f, status_f, new_name)
        i -= 1
    user_count['date'] = user_count['date'].dt.strftime('%Y-%m-%d')
    message = {}
    for column in user_count.columns:
        message[column] = user_count[column].T.values.tolist()
    return jsonify(message)


@bp.route("/chartData3")
def chartData3():
    promotions = GetPromotionModel(interval=9000)
    promotions = promotions.getSQlData()
    value, ratio = promotionChartData2(promotions, cycle="M", values=["fee", "total"], column=["user"],
                                       count=False)
    value['date'] = value['date'].dt.strftime('%Y-%m-%d')
    ratio['date'] = ratio['date'].dt.strftime('%Y-%m-%d')
    fee = value['fee']
    fee['date'] = value['date']
    total = value['total']
    total['date'] = value['date']
    message = {"fee": {}, "total": {}, "ratio": {}}
    for col in fee.columns:
        message["fee"][col] = fee[col].T.values.tolist()
    for col in total.columns:
        message["total"][col] = total[col].T.values.tolist()
    for col in ratio.columns:
        message["ratio"][col] = ratio[col].T.values.tolist()
    return jsonify(message)
