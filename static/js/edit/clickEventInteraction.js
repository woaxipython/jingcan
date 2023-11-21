$(document).ready(function () {
    writrDateInput()
    $("tbody").on('click', '.selectProCheck', function () {
        var tr = $(this).closest("tr")
        var proPlat = tr.find('td:eq(1)').text();
        var proPlatId = tr.find('td:eq(1)').find("small").data("id")
        var proMethod = tr.find('td:eq(2)').text();
        var proMethodId = tr.find('td:eq(2)').find("small").data("id")
        var url = '/sale/proinfo'
        GetRequest(url)
            .then(function (result) {
                writeStoreProInfo(proPlat, proPlatId, proMethod, proMethodId, result['data'], result['group'])
            })
            .catch(function (error) {
                alert(error)
            })
    })
    $("tbody").on('click', '.editAttention', function () {
        var tr = $(this).closest("tr")
        var search_id = tr.data('id')
        var a = $(this).find('a')
        var text = a.text()
        if (text === '关注') {
            var attention = 1
        } else {
            attention = 0
        }
        var url = '/pv/attention' + "?search_id=" + search_id + '&attention=' + attention
        GetRequest(url)
            .then(function (result) {
                a.text(result['message'])
            })
            .catch(function (error) {
                alert(error)
            })
    })

    $("tbody").on('click', '.editConstract', function () {
        var constractCode = $(this).closest("tr").data("id")
        $('input[name="constractCodeId"]').val(constractCode)
    })

    $("tbody").on('click', '.editXhs', function () {
        var tr = $(this).closest("tr")
        var token_id = tr.data('id')
        $('input[name="token_id"]').val(token_id)
    })

    $("tbody").on('click', '.edit-role', function () {
        var trId = $(this).closest("tr").data("id")
        $('input[name="editRoleId"]').val(trId)
    })

    $("body").on('click', ".del-icon", function () {
        $(this).closest("tr").remove()
        calculateTotal()
    })

    $("tbody").on('click', '.selectAtomCheck', function () {
        var tr = $(this).closest("tr")
        var orderPr = tr.find('td:eq(1)').find(".orderPr")
        var prCode = orderPr.data("id")
        var prname = orderPr.text().trim()
        if ($(this).is(':checked')) {
            writeNewSaleTable(prCode, prname)
        } else {
            delNewSaleTable(prCode)
        }
    })

    $("tbody").on('click', '.selectSaleCheck', function () {
        var tr = $(this).closest("tr")
        var orderPr = tr.find('td:eq(1)').find(".orderPr")
        var prCode = orderPr.data("id")
        var prname = orderPr.text().trim()
        if ($(this).is(':checked')) {
            writeNewGroupTable(prCode, prname)
        } else {
            delNewGroupTable(prCode)
        }
    })

    $("tbody").on('click', '.selectOrderSale', function () {
        var tr = $(this).closest("tr")
        var orderPr = tr.find('td:eq(1)').find(".orderPr")
        var prCode = orderPr.data("id")
        var prname = orderPr.text().trim()
        if ($(this).is(':checked')) {
            writeHandOrderTable(prCode, prname)
        } else {
            delHandOrderTable(prCode)
        }
    })
    $('input[name="newPurchaseFreight"]').change(function () {
        calculateTotal()
    })

    $('input[name="newPurchaseOther"]').change(function () {
        calculateTotal()
    })


    $("#addPurchaseList").click(function () {
        var form = $("#newPurchasePrForm")
        var inputs = form.find('input')
        var result = Verification(...inputs)
        if (result.length === 0) {
            let TableId = "purchaseListTable"
            writePurchaseTable(TableId)
        }
    })

    // 自动创建采购单名称
    $('select[data-select="newPurchaseUser"]').change(function () {
        console.log(123465)
        var purchaseInput = $('input[name="newPurchaseName"]')
        var purchaseName = purchaseInput.val()
        var userName = $('select[data-select="newPurchaseUser"] option:selected').text()
        if (!purchaseName) {
            var currentDate = new Date();
            var randomString = Math.random().toString(36).substring(2, 5);
            var formattedDateTime = $.datepicker.formatDate('yy-mm-dd', currentDate) + "-" + randomString;
            purchaseInput.val(userName + "-" + formattedDateTime)
        }
    })

    //监听数据展示框的事件
    $('.nav-item').click(function () {
        var close_ul = $(this).closest('ul')
        var interval_div = close_ul.find('div[data-div="cycle"]');
        interval_div.addClass('d-none');
        var clicknav = $(this).find('div')
        clicknav.removeClass('d-none')
    })

    $('select[data-select="stack"]').change(function () {
        var stack = $(this).val()

        var divID = $(this).closest('a').attr('href').replace("#", "")
        var chartsID = $("#" + divID).find('div').attr('id')
        var element = echarts.init(document.getElementById(chartsID));

        var option = element.getOption()
        // 获取当前x轴
        var xAxisData = option.xAxis[0].data
        // 获取当前Y轴的相关信息（数据、堆形等）
        var series = option.series

        // 如果是line或者是空值，就继续用折现
        $.each(series, function (key, value) {
            value.stack = stack
        })
        var saleOption = StackLineChart(xAxisData = xAxisData, seriesData = series,)
        element.setOption(saleOption);

    })
})


