$("#refreshLocation").click(function () {
    var url = '/back/refreshLocation'
    GetRequest(url = url)
        .then(function (result) {
            alert(result['message'])
        })
        .catch(function (error) {
            alert(error)
        })
})

$("#getPVContentData").click(function () {
    var url = '/promotion/refreshPromotionData'
    GetRequest(url = url)
        .then(function (result) {
            alert(result['message'])
        })
        .catch(function (error) {
            alert(error)
        })
})

$(".city-select").change(function () {
    var city = $(this).val()
    var url = '/back/getCityArea?city=' + city
    GetRequest(url = url)
        .then(function (result) {
            var area = result['message']
            var areaSelect = $(".area-select")
            areaSelect.empty()
            var option = $("<option></option>")
            option.text("请选择区")
            areaSelect.append(option)
            for (var i = 0; i < area.length; i++) {
                option = $("<option></option>")
                option.text(area[i].name)
                option.val(area[i].name)
                areaSelect.append(option)
            }
        })
        .catch(function (error) {
            alert(error)
        })
})

$("#captcha").click(function () {
    var url = "/store/kdzsCaptcha"
    GetRequest(url)
        .then(function (result) {
            $(this).find("img").remove()
            var img = $("<img>").attr("src", '../static/images/captcha.png?rand=' + Math.random()).attr("class", "w-100")
            $("#captcha").html(img)
        })
        .catch(function (error) {
            alert(error)
        })
})

$("#kdzsTest").click(function () {
    var account = $('input[name="kdzsAccount"]').val()
    console.log(account)
    var url = "/store/kdzsTest?account=" + account
    GetRequest(url)
        .then(function (result) {
            alert(result['message'])
        })
        .catch(function (error) {
            alert(error)
        })
})

$("#kdzsStore").click(function () {

    var url = "/store/kdzsStore"
    GetRequest(url)
        .then(function (result) {
            alert(result['message'])
        })
        .catch(function (error) {
            alert(error)
        })
})

function mobielCodeTimer(time_length, timerId, btnid) {
    var remainingTime = time_length;
    var intervalId = setInterval(function () {
        remainingTime--;
        if (remainingTime === 0) {
            $("#" + btnid).attr("disabled", false);
            $("#" + timerId).text("");
            clearInterval(intervalId);
        } else {
            $("#" + btnid).attr("disabled", true)
            $("#" + timerId).text("剩余时间：" + remainingTime + " 秒");
        }
    }, 1000);

}

$('#getPhoneCodeKs').click(function () {
    var url = "/back/getPhoneCodeKs"
    GetRequest(url)
        .then(function (result) {
            alert(result['message'] + " 请注意查收短信," + "120秒后可重新获取")
            mobielCodeTimer(120, "ksPhoneCodeTimer", "getPhoneCodeKs")
        })
        .catch(function (error) {
            alert(error)
        })
})

$('#testKsSpyder').click(function () {
    var url = "/back/testKs"
    GetRequest(url)
        .then(function (result) {
            alert(result['message'])
        })
        .catch(function (error) {
            alert(error)
        })
})

$('tbody').on('click', '.testXhs', function () {
    var tr = $(this).closest('tr')
    var token_id = tr.data('id')
    var url = "/back/testXhs?token_id=" + token_id
    GetRequest(url)
        .then(function (result) {
            alert(result['message'])
        })
        .catch(function (error) {
            alert(error)
        })
})

$('#testSpyderXhs').click(function () {
    var url = "/back/testXhs"
    GetRequest(url)
        .then(function (result) {
            alert(result['message'])
        })
        .catch(function (error) {
            alert(error)
        })
})

$('#testSpyderDy').click(function () {
    var url = "/back/testDy"
    GetRequest(url)
        .then(function (result) {
            alert(result['message'])
        })
        .catch(function (error) {
            alert(error)
        })
})

$("tbody").on('click', '.editPromotion', function () {
    var promotionId = $(this).closest("tr").data('id')
    $('input[name="editPromotionId"]').val(promotionId)
    url = "/promotion/search?promotionId=" + promotionId
    GetRequest(url)
        .then(function (result) {
            if (result['status'] === 'success') {
                writeEditPromotionTbale(result['message'])
            } else {
                alert(result['message'])
            }

        })
        .catch(function (error) {
            alert(error)
        })
})

function getPromotiondata() {

    var url = '/promotion/data'
    GetRequest(url)
        .then(function (result) {
            writePromotionData(result['message'])
        })
        .catch(function (error) {
            alert(error)
        })
}

$("#newGroupSearchSale").click(function () {
    var input_name = $('input[name="searchSaleName"]').val()
    if (input_name) {
        var url = '/product/searchSale?name=' + input_name
        GetRequest(url)
            .then(function (result) {
                if (result['status'] === 'success') {
                    writeGroupSale(result['message'])
                } else {
                    alert(result['message'])
                }
            })
            .catch(function (error) {
                alert(error)
            })

    }

})

// 监听周期select点击事件,并使用get请求，获取数据
$('select[data-select="cycle"]').change(function () {
    var element = echarts.init(document.getElementById('saleData'));

    var a = $(this).closest("a")
    var aHref = a.attr("href")
    var a_url = aHref.replace("#", "").replace("_", "/")
    console.log(a_url)

    var store = a.find("select[data-store='store']").val()
    if (!store) {
        store = "all"
    }

    var date = a.find("select[data-interval='interval']").val()
    if (!date) {
        date = 30
    }
    var cycle = a.find("select[data-cycle='cycle']").val()
    if (!cycle) {
        cycle = "d"
    }
    var url = '/' + a_url + "?cycle=" + cycle + '&interval=' + date + '&store=' + store
    GetRequest(url)
        .then(function (result) {
            if (aHref === '#tabs-sales') {
                element = echarts.init(document.getElementById('saleData'));
                makeSaleAllStoreShow(element, result)
            } else if (aHref === '#tabs-orders') {
                element = echarts.init(document.getElementById('orderData'));
                makeSaleAllOrderShow(element, result)
            } else if (aHref === '#sale_tabs-sales') {
                element = echarts.init(document.getElementById('saleData'));
                makeSaleStoreShow(element, result)
            } else if (aHref === '#sale_tabs-orders') {
                element = echarts.init(document.getElementById('countData'));
                makeSaleStoreCountShow(element, result)
            } else if (aHref === '#sale_tabs-pr') {
                element = echarts.init(document.getElementById('groupData'));
                makeGroupSaleShow(element, result)
            }

        })
        .catch(function (error) {
            alert(error)
        })
})