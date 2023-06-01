function GetRequest(url) {
    return new Promise(function (resolve, reject) {
        $.ajax({
            url: url,
            type: "get",
            success: function (response) {
                // 请求成功回调处理
                resolve(response);
            },
            error: function (xhr, status, error) {
                alert(error);
            }
        });
    });
}

function FormRequest(formArray, url) {
    return new Promise(function (resolve, reject) {
        $.ajax({
            url: url,// 替换成你的Flask后台URL
            type: "post", // 将inputValues作为请求数据发送到Flask后台
            data: formArray,
            success: function (response) {
                // 请求成功回调处理
                resolve(response);
            },
            error: function (xhr, status, error) {
                alert(error);
            }
        });
    });
}

function JsonRequest(data, url) {
    var csrf_token = $('meta[name=csrf-token]').attr('content');
    return new Promise(function (resolve, reject) {
        $.ajax({
            url: url,// 替换成你的Flask后台URL
            type: "post", // 将inputValues作为请求数据发送到Flask后台
            data: data,
            contentType: "application/json",
            headers: {
                "X-CSRFToken": csrf_token
            },
            success: function (response) {
                // 请求成功回调处理
                resolve(response);
            },
            error: function (xhr, status, error) {
                alert(error);
            }
        });
    });
}


function FileRequest(Form, url) {
    var csrf_token = $('meta[name=csrf-token]').attr('content');
    return new Promise(function (resolve, reject) {
        $.ajax({
            url: url, // 替换成你的Flask后台URL
            type: "POST",
            data: Form, // 将inputValues作为请求数据发送到Flask后台
            contentType: false,  // 必须设置
            processData: false,  // 必须设置
            headers: {
                "X-CSRFToken": csrf_token
            },
            success: function (response) {
                // 请求成功的回调处理
                resolve(response);
            },
            error: function (xhr, status, error) {
                alert(error);
            }
        });
    });
}