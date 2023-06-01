$('input').on('input', function () {
    var name = $(this).attr('name'); // 获取当前input的name属性值
    var value = $(this).val(); // 获取当前input的值
    $('input[name="' + name + '"]').not($(this)).val(value); // 将所有name相同的input的值设置为当前input的值
});

// 当表中的select发生改变时，触发的事件
$('.select-input').on('change', function (event) {
    event.preventDefault();
    var inputName = $(this).data("select")
    var values = $(this).val()
    $("input[name=" + inputName + "]").val(values)

});


function Verification(...inputs) {
    var status = []
    $.each(inputs, function (index, input) {
        var inputVal = $(input).val();
        var inputName = $(input).attr("name");
        if ($(input).hasClass("required")) {
            if (inputVal.trim() === '') {
                $('small[data-input=' + inputName + ']').removeClass('d-none');
                $('input[name=' + inputName + ']').addClass('is-invalid');
                status.push(0)
            } else {
                $('small[data-input=' + inputName + ']').addClass('d-none')
                $('input[name=' + inputName + ']').removeClass('is-invalid');
            }
        }
    })
    // 使用rateInput和inputs数组访问参数
    // ...
    return status
}

function VeriNumm(...dict) {
    var status = []
    $.each(dict, function (key, value) {
        $.each(value, function (key, value) {
            console.log(value)
            if (!value) {
                status.push(0)
            }
        })

    })
    // 使用rateInput和inputs数组访问参数
    // ...
    return status
}

function VeriHref(...inputs) {
    var status = []
    $.each(inputs, function (index, input) {
        var urlRegex = /(http(s)?:\/\/[^\s]+)/gi;
        var inputVal = $(input).val();
        var inputName = $(input).attr("name");
        if (!inputVal.match(urlRegex)) {
            $('.' + inputName + '-error').removeClass('d-none');
            $(input).addClass('is-invalid');
            status.push(0)
        } else {
            $('.' + inputName + '-error').addClass('d-none')
            $(input).removeClass('is-invalid');
        }
    })
    return status
}

// 验证0以上整数型
$(".integer-input").on("blur", function (event) {
    const value = $(this).val();
    const regex = /^[0-9]\d*$/;
    const inputName = $(this).attr("name")
    if (!regex.test(value)) {
        $('.' + inputName + '-error').removeClass('d-none');
        $(this).addClass('is-invalid');
        $(this).val("0").trigger('keyup');

    }
})

// 验证0-1的浮点类型，最多4位小数点
$(".zero-float-input").on("blur", function (event) {
    const value = $(this).val();
    const regex = /^(0(\.\d{1,4})?|1(\.0{1,4})?)$/;
    const inputName = $(this).attr("name")
    if (!regex.test(value)) {
        $('.' + inputName + '-error').removeClass('d-none');
        $(this).addClass('is-invalid');
        $(this).val("0").trigger('keyup');
    }
})


// 验证0以上浮点类型
$(".float-input").on("blur", function (event) {
    const value = $(this).val();
    const regex = /^[0-9]+(\.[0-9]{1,4})?$/;
    const inputName = $(this).attr("name")
    if (!regex.test(value)) {
        $('.' + inputName + '-error').removeClass('d-none');
        $(this).addClass('is-invalid');
        $(this).val("0").trigger('keyup');
    }
})

// 验证1以上浮点类型
$(".one-float-input").on("blur", function (event) {
    const value = $(this).val();
    const regex = /^[1-9]+(\.[0-9]{1,4})?$/;
    const inputName = $(this).attr("name")
    if (!regex.test(value)) {
        $('.' + inputName + '-error').removeClass('d-none');
        $(this).addClass('is-invalid');
        $(this).val("0").trigger('keyup');
    }
})



function calculateTotal() {
    var totalCost = 0;
    var totalNumber = 0
    $('#purchaseListTable tbody tr').each(function () {
        var cost = parseFloat($(this).find('td:eq(4)').text());
        var number = parseFloat($(this).find('td:eq(2)').text());
        totalCost += cost;
        totalNumber += number
    });
    $("#purchase-pr-number").text(totalNumber.toFixed(0))
    $("#total-pr-price").text(totalCost.toFixed(2))
    var freight = $('input[name="newPurchaseFreight"]').val()
    var other = $('input[name="newPurchaseOther"]').val()
    console.log(freight, other, totalCost)
    totalCost = totalCost + parseFloat(freight) + parseFloat(other)
    if (!totalCost) {
        totalCost = 0
    }
    $('#totalPrice').text(totalCost.toFixed(2))
}
