function saleAllStoreShow(element) {
    var url = '/orderData'
    GetRequest(url)
        .then(function (result) {
            var saleItem = lineCharts(name = "销售额", stack = "", type = "line")
            saleItem.data = result[1]
            var refundItem = lineCharts(name = "退款额", stack = "", type = "line")
            refundItem.data = result[3]
            var receivItem = lineCharts(name = "收款额", stack = "", type = "line")
            receivItem.data = result[5]
            var seriesItem = [saleItem, refundItem, receivItem]
            var saleOption = XOpention(xAxisData = result[0], seriesData = seriesItem,)
            element.setOption(saleOption);
        })
        .catch(function (error) {
            alert(error)
        })
}

function saleAllOrderShow(element) {
    var url = '/pOrderData';
    GetRequest(url)
        .then(function (result) {
            var saleItem = lineCharts(name = "客单价", stack = "", type = "line")
            saleItem.data = result[3]
            var refundItem = lineCharts(name = "订单量", stack = "", type = "line")
            refundItem.data = result[2]
            var seriesItem = [saleItem, refundItem]
            var saleOption = XOpention(xAxisData = result[0], seriesData = seriesItem,)
            element.setOption(saleOption);
        })
        .catch(function (error) {
            alert(error)
        })
}

function saleAllStoreBarShow(element, url = '/storeProData') {

    GetRequest(url)
        .then(function (result) {
            console.log(result)
            var seriesItem = []
            var total = 0
            $.each(result, function (i, v) {
                total += parseFloat(v[1])
            })
            $.each(result, function (i, v) {
                writeMonthOrdersDiv(v, total)
                var saleItem = lineCharts(name = v[0], stack = "total", type = "bar")
                saleItem.data = [v[1].toFixed(0)]
                seriesItem.push(saleItem)
            })
            var yAxisData = [""]
            var saleOption = YOpention(yAxisData = yAxisData, seriesData = seriesItem,)
            element.setOption(saleOption);
        })
        .catch(function (error) {
            alert(error)
        })
}

function saleMapShow(element) {
    url = '/sale/orderMap'
    GetRequest(url)
        .then(function (result) {
            var data = []
            $.each(result, function (i, v) {
                data.push({
                    name: v[0],
                    value: v[1]
                })
            })
            console.log(data)
            zGMapOption(jsonUrl = "../static/json/ZG.json", mapChart = element, data = data)
        })
        .catch(function (error) {
            alert(error)
        })
}

function saleStoreData(saleElement, countElement) {
    url = '/sale/storeData'
    GetRequest(url)
        .then(function (result) {
            var seriesItem = []
            $.each(result.total, function (key, value) {
                if (key !== 'date') {
                    var saleItem = lineCharts(name = key, stack = "total", type = "line", areaStyle = "show")
                    saleItem.data = value
                    seriesItem.push(saleItem)
                }
            })
            var saleOption = XOpention(xAxisData = result.total.date, seriesData = seriesItem,)
            saleElement.setOption(saleOption);

            seriesItem = []
            $.each(result.count, function (key, value) {
                if (key !== 'date') {
                    var saleItem = lineCharts(name = key, stack = "total", type = "line", areaStyle = "show")
                    saleItem.data = value
                    seriesItem.push(saleItem)
                }
            })
            saleOption = XOpention(xAxisData = result.count.date, seriesData = seriesItem,)
            countElement.setOption(saleOption);
        })
        .catch(function (error) {
            alert(error)
        })
}


function weekTimeChartShow(element) {

    url = '/sale/orderTimeMap'
    GetRequest(url)
        .then(function (result) {
            console.log(result)
            var data = result.data
            var days = result.days
            var hours = result.hours
            var option = weekTimeOption(hours = hours, days = days, data = data)
            element.setOption(option);
        })
        .catch(function (error) {
            alert(error)
        })
}

function writeMonthOrdersDiv(v, total) {
    if (total === 0) {
        total = 1
    }
    var month_div_show = $('#month_orders_div_show')
    var show_row = $('<div class="row pb-1 mb-1 border-bottom">')
    var avatar_div = $('<div class="col-auto"><span class="avatar">WM</span></div>')
    var sale_info_div = $('<div class="col">')
    var sale_payment_div = $(' <div class="text-truncate d-flex justify-content-between">' +
        '<strong>' + v[0] + '</strong>' +
        '<strong><span>销售额：</span>' +
        '<span>' + v[1].toFixed(0) + '</span></strong></div>')
    var sale_number_div = $('<div class="text-truncate d-flex justify-content-end">' +
        '<small class="text-muted jus"><span class="text-muted">占比：</span>' + (parseFloat(v[1]) * 100 / total).toFixed(2) +
        '%</small></div>')
    var badge_div = $('<div class="badge bg-success">')
    sale_info_div.append(sale_payment_div)
    sale_info_div.append(sale_number_div)
    show_row.append(avatar_div)
    show_row.append(sale_info_div)
    show_row.append(badge_div)
    month_div_show.append(show_row)

}

function PromotionPlatData(countChart, ValueChart) {
    var url = '/pro/chartData'
    GetRequest(url)
        .then(function (result) {
            var seriesItem = []
            $.each(result.plat, function (key, value) {
                if (key !== 'date') {
                    var saleItem = lineCharts(name = key, stack = "total", type = "line", areaStyle = "show")
                    saleItem.data = value
                    seriesItem.push(saleItem)
                }
            })
            var saleOption = XOpention(xAxisData = result.plat.date, seriesData = seriesItem,)
            countChart.setOption(saleOption);

            seriesItem = []
            $.each(result.plat_liked, function (key, value) {
                if (key !== 'date') {
                    var saleItem = lineCharts(name = key + "-点赞", stack = "", type = "line", areaStyle = "")
                    saleItem.data = value
                    seriesItem.push(saleItem)
                }
            })
            $.each(result.collected, function (key, value) {
                if (key !== 'date') {
                    var saleItem = lineCharts(name = key + "-收藏", stack = "", type = "line", areaStyle = "")
                    saleItem.data = value
                    seriesItem.push(saleItem)
                }
            })
            $.each(result.commented, function (key, value) {
                if (key !== 'date') {
                    var saleItem = lineCharts(name = key + "-评论", stack = "", type = "line", areaStyle = "")
                    saleItem.data = value
                    seriesItem.push(saleItem)
                }
            })
            saleOption = XOpention(xAxisData = result.plat_liked.date, seriesData = seriesItem,)
            ValueChart.setOption(saleOption);
        })
        .catch(function (error) {
            alert(error)
        })
}

function PromotionUserData(UserSendChart) {
    var url = '/pro/chartData2'
    GetRequest(url)
        .then(function (result) {
            var seriesItem = []
            $.each(result, function (key, value) {
                if (key !== 'date') {
                    var saleItem = lineCharts(name = key, stack = "", type = "line", areaStyle = null)
                    saleItem.data = value
                    seriesItem.push(saleItem)
                }
            })
            var saleOption = XOpention(xAxisData = result.date, seriesData = seriesItem,)
            UserSendChart.setOption(saleOption);
        })
        .catch(function (error) {
            alert(error)
        })
}

function PromotionUserData2(UserFeeChart, UserTotalChart, UserROIChart) {
    var url = '/pro/chartData3'
    GetRequest(url)
        .then(function (result) {
            console.log(result)
            var seriesItem = []
            $.each(result.fee, function (key, value) {
                if (key !== 'date') {
                    var saleItem = lineCharts(name = key, stack = "", type = "line", areaStyle = null)
                    saleItem.data = value
                    seriesItem.push(saleItem)
                }
            })
            var saleOption = XOpention(xAxisData = result.fee.date, seriesData = seriesItem,)
            UserFeeChart.setOption(saleOption);

            seriesItem = []
            $.each(result.total, function (key, value) {
                if (key !== 'date') {
                    var saleItem = lineCharts(name = key, stack = "", type = "line", areaStyle = null)
                    saleItem.data = value
                    seriesItem.push(saleItem)
                }
            })
            saleOption = XOpention(xAxisData = result.total.date, seriesData = seriesItem,)
            UserTotalChart.setOption(saleOption);

            seriesItem = []
            $.each(result.ratio, function (key, value) {
                if (key !== 'date') {
                    var saleItem = lineCharts(name = key, stack = "", type = "line", areaStyle = null)
                    saleItem.data = value
                    seriesItem.push(saleItem)
                }
            })
            saleOption = XOpention(xAxisData = result.ratio.date, seriesData = seriesItem,)
            UserROIChart.setOption(saleOption);
        })
        .catch(function (error) {
            alert(error)
        })
}

function writeTodayInfo() {
    url = '/allToadyData'
    GetRequest(url)
        .then(function (result) {
            console.log(result)
            $('#today_payment_orders').text(result.today_payment_orders)
            $('#today_refund_payment').text(result.today_refund_payment)
            $('#month_payment').text(result.month_payment)
            $('#today_express_d').text(result.today_express_d)
            $('#today_express_w').text(result.today_express_w)
            $('#today_order_count').text(result.today_order_count)
            $('#today_store_pro').text(result.today_store_pro)
            $('#today_wait_orders').text(result.today_wait_orders)
        })
        .catch(function (error) {
            alert(error)
        })
}