import pandas as pd


def mergeFrame(main_info, merge_info, type='date'):
    if type == 'date':
        main_info = pd.merge(main_info, merge_info, on='date', how='outer').fillna(0)
    else:
        main_info = pd.merge(main_info, merge_info, on='date', how='outer')
    main_info.total_y = main_info.total_y.fillna(0)
    main_info.total_x = main_info.total_x.fillna(0)
    main_info['actual'] = main_info.total_x - main_info.total_y
    return main_info


def makeOrderFrameData(sql_list, cycle="Q", store="all"):
    order = pd.DataFrame(sql_list)
    order.columns = ['date', 'store_name', 'total', 'counts']
    order['date'] = pd.to_datetime(order['date'])
    order = order.set_index('date')
    order = order.resample(cycle).sum()
    order = order.reset_index()
    order['date'] = order['date'].dt.strftime('%Y-%m-%d')
    order.total = order.total.fillna(0)
    print(order.columns)

    return order


def makePOrderAll(sql_list, cycle="M", store="all"):
    order = pd.DataFrame(sql_list)
    order.columns = ['date', 'store_name', 'total', 'counts']
    order['date'] = pd.to_datetime(order['date'])
    order = order.set_index('date')
    order = order.resample(cycle).sum()
    order['unit'] = round(order.total / order.counts, 1)
    order = order.reset_index()
    order['date'] = order['date'].dt.strftime('%Y-%m-%d')
    order.unit = order.unit.fillna(0)
    return order


def makePOrderStore(sql_list, values='total', cycle="D"):
    order = pd.DataFrame(sql_list)
    order.columns = ['date', 'store_name', 'total', 'counts']
    order['date'] = pd.to_datetime(order['date'])
    order = order.set_index('date')
    order['unit'] = round(order.total / order.counts, 1)
    order = order.reset_index()
    order = round(
        order.pivot_table(index=pd.Grouper(key='date', freq=cycle), columns='store_name', values=values,
                          aggfunc='sum').fillna(0), 0)
    order = order.reset_index()

    order['date'] = order['date'].dt.strftime('%Y-%m-%d')
    return order


def makePOrderMapAll(sql_list, total=False, count=False):
    map = pd.DataFrame(sql_list)
    map.columns = ['location', 'total', 'count']
    map = map.reset_index()
    map.loc[map['location'] == "北京", 'location'] = "北京市"
    map.loc[map['location'] == "上海", 'location'] = "上海市"
    map.loc[map['location'] == "天津", 'location'] = "天津市"
    map.loc[map['location'] == "重庆", 'location'] = "重庆市"
    map.loc[map['location'] == "香港", 'location'] = "香港特别行政区"
    map.loc[map['location'] == "澳门", 'location'] = "澳门特别行政区"
    map.loc[map['location'] == "台湾", 'location'] = "台湾省"
    map = map.groupby('location').sum()
    map = map.reset_index()
    map.drop(map[map['location'] == "**"].index, inplace=True)
    del map['index']
    if total:
        map = map.sort_values(by='total', ascending=False)
        map = map.copy().reset_index()
        del map['index']
        del map['count']
    elif count:
        map = map.sort_values(by='count', ascending=False)
        map = map.copy().reset_index()
        del map['index']
        del map['total']
    else:
        map = map.sort_values(by='total', ascending=False)
        map = map.copy().reset_index()
        del map['index']
    return map


def makePOrderTimeMapAll(sql_list, total=False, count=False):
    map = pd.DataFrame(sql_list)
    map.columns = ['date', 'total', 'count']
    map['date'] = pd.to_datetime(map['date'])
    map = map.reset_index()
    map['week'] = map['date'].dt.day_name()
    # map['week'] = map['day'].dt.day_name()
    map['time'] = map['date'].dt.hour

    map = round(map.pivot_table(index='week', columns="time", values='total', aggfunc='sum').fillna(0), 0)
    map = map.reset_index()

    return map


def makeTimeMapData(data_pd):
    week_map = {'Monday': 1, 'Tuesday': 2, 'Wednesday': 3, 'Thursday': 4, 'Friday': 5, 'Saturday': 6, 'Sunday': 7}
    data_pd['week_num'] = data_pd['week'].map(week_map)
    data_pd = data_pd.sort_values(by='week_num', ascending=False)
    # 将week列中的星期几转换为数字
    days_ZH = {
        'Monday': '星期一', 'Tuesday': '星期二', 'Wednesday': '星期三', 'Thursday': '星期四', 'Friday': '星期五',
        'Saturday': '星期六', 'Sunday': '星期日'
    }
    days = []
    data = []
    hours = [str(i) + " 点" for i in range(24)]
    map_data = data_pd.T.values.tolist()
    for i in range(len(map_data)):
        if i == 0:
            for j in range(len(map_data[i])):
                days.append(days_ZH.get(map_data[i][j]))
        else:
            for j in range(len(map_data[i])):
                hour_data = []
                if map_data[i][j] == 0:
                    map_data[i][j] = 0
                hour_data.append(i - 1)
                hour_data.append(j)
                hour_data.append(map_data[i][j])
                data.append(hour_data)
    map_data = {
        "days": days,
        "hours": hours,
        "data": data
    }
    return map_data


def makeStoreFeeAllPr(sql_list, cycle='D'):
    order = pd.DataFrame(sql_list)
    order.columns = ['date', 'store_name', 'method', 'product', 'total']
    order['date'] = pd.to_datetime(order['date'])
    order = order.set_index('date')
    order['store-method'] = order['store_name'] + '-' + order['method']
    del order['store_name']
    del order['method']
    del order['product']
    order = order.reset_index()
    order = round(
        order.pivot_table(index=pd.Grouper(key='date', freq=cycle), columns='store-method', values='total',
                          aggfunc='sum').fillna(0), 0)
    order = order.reset_index()
    order['date'] = order['date'].dt.strftime('%Y-%m-%d')
    return order
