function writrDateInput() {
    var today = new Date();
    var year = today.getFullYear()
    var month = (today.getMonth() + 1).toString().padStart(2, "0")
    var day = today.getDate().toString().padStart(2, "0")
    var date = year + '-' + month + "-" + day;
    $('input[name="kdzsEndDate"]').val(new Date().toISOString().slice(0, -8));
    var severLaterDays = new Date((new Date()).setDate((new Date()).getDate() - 1)).toISOString().slice(0, -8)
    $('input[name="kdzsStartDate"]').val(severLaterDays);
}

function splitStr() {
    return "ikd6l60q"
}

function delIcon() {
    return $('<span class="text-danger hover-shadow hover cursor-pointer del-icon">\
                                            <svg xmlns="http://www.w3.org/2000/svg"\
                                                 class="icon icon-tabler icon-tabler-square-off" width="24"\
                                                 height="24"\
                                                 viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" fill="none"\
                                                 stroke-linecap="round"\
                                                 stroke-linejoin="round">\
                                            <path stroke="none" d="M0 0h24v24H0z" fill="none"></path>\
                                            <path\
                                                d="M8 4h10a2 2 0 0 1 2 2v10m-.584 3.412a2 2 0 0 1 -1.416 .588h-12a2 2 0 0 1 -2 -2v-12c0 -.552 .224 -1.052 .586 -1.414"></path>\
                                            <path d="M3 3l18 18"></path></svg></span>')
}

function upIcon() {
    return $('<span class="text-primary">\
            <svg xmlns="http://www.w3.org/2000/svg" class="icon icon-tabler icon-tabler-arrow-narrow-up" width="24" \
            height="24" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" fill="none" \
            stroke-linecap="round" stroke-linejoin="round">\
           <path stroke="none" d="M0 0h24v24H0z" fill="none"></path>\
           <path d="M12 5l0 14"></path>\
           <path d="M16 9l-4 -4"></path>\
           <path d="M8 9l4 -4"></path>\
        </svg>\
</span>')
}

function downIcon() {
    return $('<span class="text-danger">\
            <svg xmlns="http://www.w3.org/2000/svg" class="icon icon-tabler icon-tabler-arrow-narrow-down" width="24" \
            height="24" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" fill="none" \
            stroke-linecap="round" stroke-linejoin="round">\
            <path stroke="none" d="M0 0h24v24H0z" fill="none"></path>\
            <path d="M12 5l0 14"></path>\
            <path d="M16 15l-4 4"></path>\
            <path d="M8 15l4 4"></path>\
</svg>\
</span>')
}

function dataIcon() {
    return $('<span class="text-danger  hover-shadow hover p-1" data-bs-toggle="tooltip" data-bs-placement="top" \
    aria-label="数据展示功能待开发" data-bs-original-title="数据展示功能待开发">\
        <svg xmlns="http://www.w3.org/2000/svg" class="icon icon-tabler icon-tabler-antenna-bars-5" width="24" height="24" \
        viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" fill="none" \
        stroke-linecap="round" stroke-linejoin="round">\
        <path stroke="none" d="M0 0h24v24H0z" fill="none"></path>\
        <path d="M6 18l0 -3"></path>\
        <path d="M10 18l0 -6"></path>\
        <path d="M14 18l0 -9"></path>\
        <path d="M18 18l0 -12"></path>\
        </svg>\
        </span>')
}

// 选择店铺推广花费形式
function writeStoreProInfo(proPlat, proPlatId, proMethod, proMethodId, data, group) {
    let table = $("#storeProTable")

    let store_plat = '<small class="text-muted"><div>' + proPlat + '</div><span>' + proMethod + '</span></small>'
    let store = $('<small>')
    let store_select = $('<select name="" class="form-select-sm form-select" data-id="store" style="min-width: 8rem;">' +
        '<option value="" selected disabled>选择店铺</option>')
    $.each(data, function (index, item) {
        if (item.plat.trim() === proPlat.trim()) {
            store_select.append('<option value=' + item.storeID + '>' + item.storeName + '</option>')
        }
    })
    store.append(store_select)
    let td2 = $("<div>")
    let td2number = $('<input type="number" class="form-control-sm form-control" style="min-width: 5rem;" placeholder="金额">')
    let td2product = $('<small>')
    let td2productSelect = $('<select name="" class="form-select-sm form-select" style="min-width: 6rem;"data-id="product">' +
        '<option value="0" selected disabled>选择商品</option></select>')
    $.each(group, function (index, item) {
        td2productSelect.append('<option value="' + item.id + '">' + item.name + '</option>')
    })
    td2product.append(td2productSelect)
    td2.append(td2product, td2number)
    let date = $('<input type="date" class="form-control-sm form-control">')
    let tr = $('<tr data-id=' + proPlatId + splitStr() + proMethodId + '>').append(
        $("<td>").html(delIcon),
        $("<td>").html(store_plat),
        $("<td>").html(store),
        $("<td>").append(td2),
        $("<td>").append(date),
    )
    table.append(tr)
}

function delWriteStoreProInfo(proPlatId, proMethodId) {
    let tr = $('tr[data-id=' + proPlatId + splitStr() + proMethodId + ']')
    tr.remove()
}

function writePromotionAccount(message) {
    var promotionPlatId = $('input[name="chosePlat"]').val()
    var promotionPlat = $('select[data-select="chosePlat"] option:selected').text()
    var OutPutModelId = $('input[name="choseOutPutModel"]').val()
    var OutPutModel = $('select[data-select="choseOutPutModel"] option:selected').text()
    let table = $("#promotionAccountTable")
    let title = '<div style="width: 8rem" class="me-2 text-truncate">\
    <small class="text-nowrap" >\
        <div><span data-id=' + promotionPlatId + '>' + promotionPlat + '</span></div>\
        <div><a href=' + message.profile_link + ' data-id=' + message.account_id + '><span>' + message.nickname + '</span></a></div>\
        <div><code data-id=' + OutPutModelId + '>' + OutPutModel + '</code></div>\
    </small></div>'
    let dataShow = '<small>\
        <div class="text-truncate ms-0" style="width: 15rem">\
            <small class="text-muted"><span>粉:</span>\
            <span class="me-1">' + message.fans + '</span>\
            <span class="me-1">赞:</span>\
            <span class="me-1">' + message.liked + '</span>\
            <span class="me-1">藏:</span>\
            <span>' + message.collected + '</span><br>\
            <span>图文:</span>\
            <span>' + message.notes + '</span>\
            </small>\
        </div>\
        <div class="text-truncate" style="width: 15rem">\
            <small class="text-muted"><span>粉均赞</span>\
            <span class="me-1">' + message.liked_rate + '</span>\
            <span>粉均藏</span>\
            <span>' + message.collected_rate + '</span></small>\
            </div>\
        <div class= "text-truncate" style = "width: 15rem" >\
        <small class="text-muted"><span>图文均赞</span>\
        <span class="me-1">' + message.ave_liked + '</span>\
        <span>图文均藏</span>\
        <span>' + message.ave_collected + '</span>\
        </small></div>'
    let desc = '<p>' +
        '<small class="text-muted" style="min-width: 8rem">' + message.desc + '</small><br>' +
        '<span class="badge bg-danger"></span><code class="text-muted">' + message.officialVerifyName + '</code>' +
        '</p>'
    let tr = $('<tr data-id=' + promotionPlatId + splitStr() + OutPutModelId + splitStr() + message.account_id + '>').append(
        $("<td>").html(title),
        $("<td>").html(dataShow),
        $("<td>").html(desc),
        $("<td>").html(delIcon),
    )
    table.append(tr)
}


function writeHandOrderTable(prCode, prname) {
    let table = $("#handOrderTable")
    let title = '<small class="text-muted">\
        <div class="text-truncate" style="width: 6rem">\
            <div data-id=' + prCode + ' class="OrderPr">\
                <span>' + prname + '</div>\
            <div><span>编码:</span><code>' + prCode + '</code></div>\
        </div>\
    </small>'
    let numberInput = '<div><input type="number" class="form-control" data-id="number" value="1"></div>'
    let priceInput = '<div><input type="number" step="0.01" class="form-control" data-id="price"></div>'
    let tr = $('<tr data-id=' + prCode + splitStr() + prname + '>').append(
        $("<td>").html(delIcon),
        $("<td>").html(title),
        $("<td>").html(numberInput),
        $("<td>").html(priceInput)
    )
    table.append(tr)

}

function delHandOrderTable(prCode) {
    let tr = $('tr[data-id=' + prCode + ']')
    tr.remove()
}

function writeNewSaleTable(prCode, prname) {
    let table = $("#createNewSaleTable")
    let title = '<small class="text-muted">\
        <div class="text-truncate" style="width: 6rem">\
            <div data-id=' + prCode + ' class="OrderPr">\
                <span>' + prname + '</div>\
            <div><span>编码:</span><code>' + prCode + '</code></div>\
        </div>\
    </small>'
    let numberInput = '<div><input type="number" class="form-control"></div>'
    let tr = $('<tr data-id=' + prCode + '>').append(
        $("<td>").html(delIcon),
        $("<td>").html(title),
        $("<td>").html(numberInput)
    )
    table.append(tr)
}

function delNewSaleTable(prCode) {
    let tr = $('tr[data-id=' + prCode + ']')
    tr.remove()
}

function writeNewGroupTable(prCode, prname) {
    let table = $("#newGroupTable")
    let title = '<small class="text-muted">\
        <div>\
            <div data-id=' + prCode + ' class="OrderPr">\
                <span>' + prname + '</div>\
            <div><span>编码:</span><code>' + prCode + '</code></div>\
        </div>\
    </small>'
    let tr = $('<tr data-id=' + prCode + '>').append(
        $("<td>").html(delIcon),
        $("<td>").html(title),
    )
    table.append(tr)
}

function delNewGroupTable(prCode) {
    let tr = $('tr[data-id=' + prCode + ']')
    tr.remove()
}


function writeGeneralShowDiv(divId) {
    var showDiv = $("#" + divId)
    var writeContent = '<div class="row">\
        <div class="col-auto">\
            <span class="avatar">WM</span>\
        </div>\
        <div class="col">\
            <div class="text-truncate d-flex justify-content-between">\
                <a data-bs-toggle="tooltip"\
                   data-bs-placement="right"\
                   title="跳转功能待开发">\
                    <strong>万明天猫旗舰店</strong></a>\
                <strong>销售额：21.32万</strong>\
            </div>\
            <div class="text-truncate d-flex justify-content-end">\
                <small class="text-muted jus"><span>更新时间：</span>2023/05-10</small>\
            </div>\
        </div>\
        <div class="col-auto align-self-center">\
            <div class="badge bg-primary"></div>\
        </div>\
    </div>'
    showDiv.append(writeContent)
}

function writeGeneralShowTable(tableId) {
    var table = $("#" + tableId)
    let ImgShow = '<span class="avatar avatar-sm " data-bs-toggle="tooltip" data-bs-placement="top"\
                      style="background-image: url(../static/images/avatars/000m.jpg)" aria-label="手工胶水"\
                      data-bs-original-title="手工胶水"></span>'
    let codeShow = '<div class="ms-2">\
                <small class="">手工胶水</small>\
                <small class="text-muted d-block"><span>编码：</span><span>010001</span></small>\
            </div>'
    let writeTitle = $('<div class="d-flex  align-items-center">').append(ImgShow, codeShow)
    let td1Number = '<span class="text-nowrap ms-0 me-1" href="">50单</span>'
    let td1ChangeNumber = '<small class="text-muted">50%</small>'
    let td1Icon = upIcon()
    td1Icon.append(td1ChangeNumber)
    let td1 = $('<div class="d-flex justify-content-center">').append(td1Number, td1Icon)
    let td2Number = '<span class="text-nowrap ms-0 me-1" href="">50单</span>'
    let td2ChangeNumber = '<small class="text-muted">50%</small>'
    let td2Icon = downIcon()
    td2Icon.append(td2ChangeNumber)
    let td2 = $('<div class="d-flex justify-content-center">').append(td2Number, td2Icon)
    let td3Icon = dataIcon()
    let td3 = $('<div class="d-flex justify-content-center">').append(td3Icon)
    var tr = $("<tr>").append(
        $("<td class='w-auto'>").html(writeTitle),
        $("<td class='w-2'>").html(td1),
        $("<td class='w-2'>").html(td2),
        $("<td>").html(td3),
    )
    table.append(tr)
}

function writePromotionoManageTable(tableId) {
    let table = $("#" + tableId)
    let td0 = $('<input class="form-check-input m-0 align-middle" type="checkbox" aria-label="Select invoice">')
    let td1 = '<span class="text-muted">001401</span>'
    let td2 = '<small class="text-reset">Design Works</small>'
    let td3 = $('<div style="width:300px" class="text-truncate m-0">')
    let td3Account = $('<div><small class="text-muted">小红书:</small></div>')
    let td3AccountLink = $('<a href="" class="">深圳一枝花llllad阿</a>')
    td3Account.append(td3AccountLink)
    let td3Pr = $('<div class="text-truncate text-muted"><small>合作产品:</small>')
    let td3PrInfo = $('<small><span>手工胶水 </span><span>手办胶水</span></small>')
    td3Pr.append(td3PrInfo)
    td3.append(td3Account, td3Pr)
    let td4 = $('<div>')
    let td4ImgDiv = $('<div class="text-truncate cursor-pointer" style="width: 230px"></div>')
    let td4ImgDivLink = $('<a href="">87956621 65406540654065406540人我让我让为qwerqwer千万人qwer千万人</a>')
    td4ImgDiv.append(td4ImgDivLink)
    let td4Data = $('<div class="text-truncate" style="width: 280px">')
    let td4DataDate = $('<small class="me-1"><span>发布时间：</span><span>2023-05-11</span></small>')

    let td4DataData = $('<small class="text-muted">' +
        '<span>赞:</span><span>5000</span' +
        '><span>藏:</span><span>5000</span>' +
        '<span>评:</span><span>5000</span>' +
        '</small>')
    td4Data.append(td4DataDate, td4DataData)
    td4.append(td4ImgDiv, td4Data)
    let td5 = $('<div>')
    let td5Fee = $('<div><small><span class="text-muted">付费 </span></small><span>500</span><span>元</span></div>')
    let td5Com = $('<div><small><span class="text-muted">佣金 </span></small><span>50</span><span>%</span></div>')
    td5.append(td5Fee, td5Com)
    let td6 = $('<div><span class="badge bg-success me-1"></span>待约稿</div>')
    let td7 = $('<div><a data-fslightbox="gallery" href="../static/images/photos/finances-us-dollars-and-bitcoins-currency-money-3.jpg">' +
        '<div class="img-responsive img-responsive-16x9 rounded-3 border" ' +
        'style="background-image: url(../static/images/photos/finances-us-dollars-and-bitcoins-currency-money-3.jpg)"></div>' +
        '</a></div>')
    let td9 = $('<a href="" data-bs-toggle="modal" data-bs-target="#edit-promotion-report" aria-label="Create new report">编辑</a>')
    let tr = $('<tr>').append(
        $('<td>').html(td0),
        $('<td>').html(td1),
        $('<td>').html(td2),
        $('<td>').html(td3),
        $('<td>').html(td4),
        $('<td>').html(td5),
        $('<td>').html(td6),
        $('<td>').html(td7),
        $('<td>').html(dataIcon()),
        $('<td class="text-center">').html(td9),
    )
    table.append(tr)

}

function writeEditPromotionTbale(message) {
    console.log(message)
    let table = $("#editPromotionTable")
    table.find('tbody').empty()
    message = message[0]
    $('#editPromotionWechat').text(message.bloger.wechat)
    $('#editPromotionFeeModel').text(message.feeModel.name)
    $('#editPromotionUser').text(message.user.name)
    $('#editPromotionPr').empty()
    $.each(message.group, function (index, group) {
        $('#editPromotionPr').append('<span class="badge bg-danger me-1"></span><span>' + group.name + '</span>')
    })
    var i = 0
    $.each(message.pvcontent, function (index, pvcontent) {
        let td1 = $('<div class="text-truncate" style="width: 6rem;">')
        let td1Plat = $('<div><small class="text-nowrap">' + message.account[i].plat.name + '</small></div>')
        let td1Account = $('<div><small class="text-nowrap"><a href=' + message.account[i].profile_link + '>' + message.account[i].name + '</a></small></div>')
        td1.append(td1Plat, td1Account)
        let td2 = $('<div>' +
            '<input type="text" class="form-control" name="videoLink">' +
            '<small class="form-text text-danger d-none videoImgLink-error">请输入正确带有href的链接地址</small></div>')
        let td3 = $('<div class="text-truncate cursor-pointer" style="width: 230px">')
        if (pvcontent.content_link) {
            var title = pvcontent.title
            var link = pvcontent.content_link
        } else {
            title = '尚未同步'
            link = '#'
        }
        let td3Title = $('<div><a href=' + link + '>' + title + '</a></div>')
        td3.append(td3Title)
        let td4 = $('<button class="btn  btn-primary getNotesInfo">同步</button>')
        let tr = $('<tr data-id=' + message.id + splitStr() + message.account[i]['id'] + splitStr() + pvcontent.id + '>').append(
            $('<td>').html(td1),
            $('<td class="w-25">').html(td2),
            $('<td>').html(td3),
            $('<td>').html(td4),
        )
        table.append(tr)
    })
}

function writePurchaseTable(tableId) {
    var pr_id = $('input[name="purchasePr"]').val()
    var pr_name = $('select[data-select="purchasePr"] option:selected').text()
    var suppiler_id = $('input[name="newPurchaseSupplier"]').val()
    var suppiler_name = $('select[data-select="newPurchaseSupplier"] option:selected').text()
    var number = $('input[name="newPurchaseNumber"]').val()
    var price = $('input[name="newPurchasePrice"]').val()
    var total = (parseFloat(number) * parseFloat(price)).toFixed(2)
    let table = $("#" + tableId)
    var td1 = $('<div class="text-truncate" style="width: 5rem;"><small data-id=' + pr_id + '>' + pr_name + '</small></div>')
    var td2 = $('<div class="text-truncate" style="width: 5rem;"><small data-id=' + suppiler_id + '>' + suppiler_name + '</small></div>')
    var td3 = $('<div class="text-truncate" style="width: 5rem;"><small data-id=' + number + '>' + number + '</small></div>')
    var td4 = $('<div class="text-truncate" style="width: 5rem;"><small data-id=' + price + '>' + price + '</small></div>')
    var td5 = $('<div class="text-truncate" style="width: 5rem;"><small>' + total + '</small></div>')
    var tr = $("<tr>").append(
        $("<td>").html(td1),
        $("<td>").html(td2),
        $("<td>").html(td3),
        $("<td>").html(td4),
        $("<td>").html(td5),
        $("<td>").html(delIcon()),
    )
    table.append(tr)
    calculateTotal()

}

function writePromotionData(data) {
    var have_send = $('#have_send')
    have_send.text(data[0])
    var wait_send = $('#wait_send')
    wait_send.text(data[1])
    var normal = $('#normal')
    normal.text(data[2])
    var abnormal = $('#abnormal')
    abnormal.text(data[3])
    var all_bloger = $('#all_bloger')
    all_bloger.text(data[4])
    var important_bloger = $('#important_bloger')
    important_bloger.text(data[5])
    var all_pvcontent = $('#all_pvcontent')
    all_pvcontent.text(data[6])
    var important_pvcontent = $('#important_pvcontent')
    important_pvcontent.text(data[7])
    writeWaitSendPro(data[8])
    writeAbnormalPro(data[9])
    writeImportantBlogerPro(data[10])
    writeImportantPro(data[11])
}

function writeWaitSendPro(wait_list) {
    var table = $('#waitSendProTable')
    table.find('tbody').empty()
    $.each(wait_list, function (index, wait) {
        var tr = $('<tr>').append(
            $('<td>').text(wait[0]),
            $('<td>').text(wait[1]),
            $('<td>').text(wait[2]),
            $('<td>').text(wait[3]),
            $('<td>').text(wait[4]),
            $('<td>').text(wait[5]),
            $('<td>').text(wait[6]),
            $('<td>').text(wait[7]),
            $('<td>').text(wait[8]),
            $('<td>').text(wait[9]),
            $('<td>').text(wait[10]),
        )
        table.append(tr)

    })
}

function writeAbnormalPro(abnormal) {
    var table = $('#abnormalProTable')
    table.find('tbody').empty()
    $.each(abnormal, function (index, wait) {
        var tr = $('<tr>').append(
            $('<td>').text(wait[0]),
            $('<td>').text(wait[1]),
            $('<td>').text(wait[2]),
            $('<td>').text(wait[3]),
            $('<td>').text(wait[4]),
            $('<td>').text(wait[5]),
            $('<td>').text(wait[6]),
            $('<td>').text(wait[7]),
            $('<td>').text(wait[8]),
            $('<td>').text(wait[9]),
            $('<td>').html('<a href=' + wait[11] + '>' + wait[10] + '</a>'),
            $('<td>').text(wait[12]),
            $('<td>').text(wait[13]),
            $('<td>').text(wait[14]),
        )
        table.append(tr)
    })
    $('#abnormalProTable').DataTable({
        "paging": true,
        "lengthChange": false,
        "searching": false,
        "ordering": true,
        "info": false,
    });
}

function writeImportantPro(abnormal) {
    var table = $('#importantProTable')
    table.find('tbody').empty()
    $.each(abnormal, function (index, wait) {
        var tr = $('<tr>').append(
            $('<td>').text(wait[0]),
            $('<td>').text(wait[1]),
            $('<td>').text(wait[2]),
            $('<td>').text(wait[3]),
            $('<td>').text(wait[4]),
            $('<td>').text(wait[5]),
            $('<td>').text(wait[6]),
            $('<td>').text(wait[7]),
            $('<td>').text(wait[8]),
            $('<td>').text(wait[9]),
            $('<td>').html('<a href=' + wait[11] + '>' + wait[10] + '</a>'),
            $('<td>').text(wait[12]),
            $('<td>').text(wait[13]),
            $('<td>').text(wait[14]),
        )
        table.append(tr)
    })
    $('#importantProTable').DataTable({
        "paging": true,
        "lengthChange": false,
        "searching": false,
        "ordering": true,
        "info": false,
    });
}

function writeImportantBlogerPro(bloger) {
    var table = $('#importBlogerTable')
    table.find('tbody').empty()
    $.each(bloger, function (index, wait) {
        var tr = $('<tr>').append(
            $('<td>').text(wait[0]),
            $('<td>').text(wait[1]),
            $('<td>').text(wait[2]),
            $('<td>').text(wait[3]),
            $('<td>').text(wait[4]),
        )
        table.append(tr)
    })
}