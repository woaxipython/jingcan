function saleAllStoreShow(element) {
    var url = '/orderData'
    GetRequest(url)
        .then(function (result) {
            makeSaleAllStoreShow(element, result)
        })
        .catch(function (error) {
            alert(error)
        })
}

function makeSaleAllStoreShow(element, result) {
    var saleItem = lineCharts(name = "销售额", stack = "", type = "line")
    saleItem.data = result[1]
    var refundItem = lineCharts(name = "退款额", stack = "", type = "line")
    refundItem.data = result[3]
    var receivItem = lineCharts(name = "收款额", stack = "", type = "line")
    receivItem.data = result[5]
    var seriesItem = [saleItem, refundItem, receivItem]
    var saleOption = StackLineChart(xAxisData = result[0], seriesData = seriesItem,)
    element.setOption(saleOption);

}

function saleAllOrderShow(element) {
    var url = '/pOrderData';
    GetRequest(url)
        .then(function (result) {
            makeSaleAllOrderShow(element, result)
        })
        .catch(function (error) {
            alert(error)
        })
}

function makeSaleAllOrderShow(element, result) {
    var saleItem = lineCharts(name = "客单价", stack = "", type = "line")
    saleItem.data = result[3]
    var refundItem = lineCharts(name = "订单量", stack = "", type = "line")
    refundItem.data = result[2]
    var seriesItem = [saleItem, refundItem]
    var saleOption = StackLineChart(xAxisData = result[0], seriesData = seriesItem,)
    element.setOption(saleOption);
}

function saleAllStoreBarShow(element, url = '/storeProData') {
    GetRequest(url)
        .then(function (result) {
            makeSaleAllStoreBarShow(element, result)
        })
        .catch(function (error) {
            alert(error)
        })
}

function makeSaleAllStoreBarShow(element, result) {
    var seriesItem = []
    var total = 0
    var total_id = $("#month_payment")

    $.each(result, function (i, v) {
        total += parseFloat(v[1])
    })
    total_id.text(total.toFixed(0))
    $.each(result, function (i, v) {
        writeMonthOrdersDiv(v, total)
        var saleItem = lineCharts(name = v[0], stack = "total", type = "bar")
        saleItem.data = [v[1].toFixed(0)]
        seriesItem.push(saleItem)
    })
    var yAxisData = [""]
    var saleOption = YOpention(yAxisData = yAxisData, seriesData = seriesItem,)
    element.setOption(saleOption);
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
            zGMapOption(jsonUrl = "../static/json/ZG.json", mapChart = element, data = data)
        })
        .catch(function (error) {
            alert(error)
        })
}

function saleStoreData() {
    url = '/sale/storeData'
    var saleChart = echarts.init(document.getElementById('saleData'));
    var countChart = echarts.init(document.getElementById('countData'));
    GetRequest(url)
        .then(function (result) {
            makeSaleStoreShow(saleChart, result)
            makeSaleStoreCountShow(countChart, result)
        })
        .catch(function (error) {
            alert(error)
        })
}

function makeSaleStoreShow(element, result) {
    var seriesItem = []
    $.each(result.total, function (key, value) {
        if (key !== 'date') {
            var saleItem = lineCharts(name = key, stack = "total", type = "line", areaStyle = "show")
            saleItem.data = value
            seriesItem.push(saleItem)
        }
    })
    var saleOption = StackLineChart(xAxisData = result.total.date, seriesData = seriesItem,)
    element.setOption(saleOption);
}

function makeSaleStoreCountShow(element, result) {
    var seriesItem = []
    $.each(result.count, function (key, value) {
        if (key !== 'date') {
            var saleItem = lineCharts(name = key, stack = "total", type = "line", areaStyle = "show")
            saleItem.data = value
            seriesItem.push(saleItem)
        }
    })
    saleOption = StackLineChart(xAxisData = result.count.date, seriesData = seriesItem,)
    element.setOption(saleOption);
}

function GroupSaleShow() {
    var url = '/sale/tabs-pr?cycle=d&interval=30&store=all'
    GetRequest(url)
        .then(function (result) {
            var element = echarts.init(document.getElementById('groupData'));
            makeGroupSaleShow(element, result)
        })
        .catch(function (error) {
            alert(error)
        })
}

function makeGroupSaleShow(element, result) {
    var seriesItem = []
    $.each(result.total, function (key, value) {
        if (key !== 'date') {
            var saleItem = lineCharts(name = key, stack = "total", type = "line", areaStyle = "show")
            saleItem.data = value
            seriesItem.push(saleItem)
        }
    })
    var saleOption = StackLineChart(xAxisData = result.total.date, seriesData = seriesItem,)
    element.setOption(saleOption);
}

function weekTimeChartShow(element) {

    url = '/sale/orderTimeMap'
    GetRequest(url)
        .then(function (result) {
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

function PromotionData() {
    url = '/promotion/dayData'
    var likedChart = echarts.init(document.getElementById('likedPrData'));
    var PrChart = echarts.init(document.getElementById('prData'));

    GetRequest(url)
        .then(function (result) {
            makeLikedShow(likedChart, result['data'])
            makePrDataShow(PrChart, result['data'])

        })
        .catch(function (error) {
            alert(error)
        })
}

function makePrDataShow(element, result) {
    var seriesItem = []
    $.each(result.count, function (key, value) {
        if (key !== 'date') {
            var saleItem = lineCharts(name = key, stack = "total", type = "line", areaStyle = "show")
            saleItem.data = value
            seriesItem.push(saleItem)
        }
    })
    var saleOption = StackLineChart(xAxisData = result.date, seriesData = seriesItem,)
    element.setOption(saleOption);
}

function makeLikedShow(element, result) {
    var seriesItem = []
    $.each(result.liked, function (key, value) {
        if (key !== 'date') {
            var saleItem = lineCharts(name = key + "_点赞", stack = "total", type = "line", areaStyle = "show")
            saleItem.data = value
            seriesItem.push(saleItem)
        }
    })
    $.each(result.collected, function (key, value) {
        if (key !== 'date') {
            var saleItem = lineCharts(name = key + "_收藏", stack = "total", type = "line", areaStyle = "show")
            saleItem.data = value
            seriesItem.push(saleItem)
        }
    })
    $.each(result.commented, function (key, value) {
        if (key !== 'date') {
            var saleItem = lineCharts(name = key + "_评论", stack = "total", type = "line", areaStyle = "show")
            saleItem.data = value
            seriesItem.push(saleItem)
        }
    })
    var saleOption = StackLineChart(xAxisData = result.date, seriesData = seriesItem,)
    element.setOption(saleOption);
}

function InitializationCycle() {
    var cycle_div = $("[data-div='cycle']");
    cycle_div.addClass('d-none');
    $('a[href="#tabs-sales"]').find('div').removeClass('d-none')
    $('a[href="#sale_tabs-sales"]').find('div').removeClass('d-none')
}

function writeTodayInfo() {
    url = '/allToadyData'
    GetRequest(url)
        .then(function (result) {
            $('#today_payment_orders').text(result.today_payment_orders)
            $('#today_refund_payment').text(result.today_refund_payment)
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


function writePrmotionData() {
    url = '/promotion/data'
    GetRequest(url)
        .then(function (result) {
            $('#pr_count').text(result['message'].counted)
            $('#pr_liked').text(result['message'].liked)
            $('#pr_collected').text(result['message'].collected)
            $('#pr_commented').text(result['message'].commented)
        })
}