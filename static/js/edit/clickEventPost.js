$(document).ready(function () {
    $("input[name='PromotionCheck']").click(function () {
        if ($(this).is(':checked')) {
            $('input[name="PromotionCheck"]').val("1")
            $('input[name="promotionOrder"]').prop('disabled', false);
        } else {
            $('input[name="PromotionCheck"]').val("0")
            $('input[name="promotionOrder"]').prop('disabled', true);
        }
    })

    $("input[name='editPromotionCheck']").click(function () {
        if ($(this).is(':checked')) {
            $('input[name="editPromotionCheck"]').val("1")
            $('input[name="editPromotionOrderId"]').prop('disabled', false);
        } else {
            $('input[name="editPromotionCheck"]').val("0")
            $('input[name="editPromotionOrderId"]').prop('disabled', true);
        }
    })
    // 批量上传推广花费
    $("#uploadAdFile").click(function () {
        const file = $('input[name="storePromotionFile"]')[0].files[0];
        var url = "/sale/getStoreProFile"
        const formData = new FormData();
        formData.append('file', file);
        FileRequest(formArray = formData, url = url)
            .then(function (result) {
                alert(result['message'])
            })
            .catch(function (error) {
                alert(error)
            })
    })

    // 上传手动输入的推广花费
    $("#uploadStoreAd").click(function () {
        var data = {}
        data["AdList"] = []
        var status = []
        var info = true
        $("#storeProTable tr").each(function (index, tr) {
            if (index !== 0) {
                var Ad = {}
                console.log(tr)
                var trId = $(this).data("id").split(splitStr())
                Ad["plat"] = trId[0]
                Ad["method"] = trId[1]
                Ad["store"] = $('select[data-id="store"]').val()
                Ad["product"] = $('select[data-id="product"]').val()
                Ad["fee"] = $(this).find('input[type=number]').val()
                Ad["date"] = $(this).find('input[type=date]').val()
                console.log(Ad)
                status = VeriNumm(Ad)
                if (status.length !== 0) {
                    alert("数值不能为空")
                    info = false
                    return false;
                } else {
                    data["AdList"].push(Ad)
                }
            }
        })
        if (info) {
            data = JSON.stringify(data)
            var url = '/sale/getStoreData'
            JsonRequest(data, url)
                .then(function (result) {
                    alert(result['message'])
                })
                .catch(function (error) {
                    alert(error)
                })
        }
    })

    // 增加推广账号
    $('#addPromotionAccount').click(function () {
        var Form = $("#chosePromotionAccountForm")
        const formData = new FormData();
        var profileLink = $('input[name="profileLink"]')
        var platId = $('input[name="chosePlat"]').val()
        formData.append('profileLink', profileLink.val());
        formData.append('platId', platId);
        var inputs = Form.find("input")

        var VerResult = Verification(...inputs)
        if (VerResult.length === 0) {

            var hrefResult = VeriHref(...profileLink)
            if (hrefResult.length === 0) {
                var url = '/promotion/getAccount'
                FileRequest(formData, url)
                    .then(function (result) {
                        if (result['status'] === "success") {
                            writePromotionAccount(result['message'])
                        } else {
                            alert(result['message'])
                        }
                    })
                    .catch(function (error) {
                        alert(error)
                    })
            } else {
                alert("链接格式不正确")
            }

        }
    })

    $("tbody").on('click', '.getNotesInfo', function () {
        var tr = $(this).closest("tr")
        var linkInput = tr.find("input")
        var promotion_id = tr.data('id').split(splitStr())[0]
        var account_id = tr.data('id').split(splitStr())[1]
        var note_id = tr.data('id').split(splitStr())[2]
        const formData = new FormData();
        formData.append('promotion_id', promotion_id);
        formData.append('account_id', account_id);
        formData.append('note_id', note_id);
        formData.append('noteLink', linkInput.val());
        var url = "/promotion/getNotes"
        var VeriResult = VeriHref(...linkInput)
        if (VeriResult.length === 0) {
            FileRequest(formData, url)
                .then(function (result) {
                    if (result['status'] === 'success') {
                        alert(11223)
                        // writeEditPromotionTbale(result['message'])
                    } else {
                        alert(result['message'])
                    }

                })
                .catch(function (error) {
                    alert(error)
                })
        }
    })

    // 创建新推广
    $('#createNewPromotion').click(function () {
        var Form = $("#createNewPromotionForm")
        var inputs = Form.find("input")
        var VerResult = Verification(...inputs)
        var data = {}
        data["promotionPr"] = $("#newPromotionPrSlect").val()
        data["AccountList"] = []

        if (VerResult.length === 0 && data["promotionPr"].length !== 0) {
            var formData = Form.serializeArray();
            $.each(formData, function (index, field) {
                data[field.name] = field.value;
            });
            $("#promotionAccountTable tr").each(function (index, tr) {
                if (index !== 0) {
                    var a = {}
                    var trId = $(this).data("id").split(splitStr())
                    a["plat"] = trId[0]
                    a["outputModel"] = trId[1]
                    a["account"] = trId[2]
                    data["AccountList"].push(a)
                }
            })
            data = JSON.stringify(data)
            var url = '/promotion/new'
            JsonRequest(data, url)
                .then(function (result) {
                    alert(result['message'])
                })
                .catch(function (error) {
                    alert(error)
                })

        } else {
            alert("请选择产品")
        }
    })

    // 上传推广订单号以及付费图
    $("#editPromotionUploadBtn").click(function () {
        var formData = new FormData(document.getElementById("editPromotionForm"));
        var file = $('input[name="FeeImgFile"]')[0].files[0];
        formData.append('file', file);
        var url = "/promotion/edit"
        FileRequest(formArray = formData, url = url)
            .then(function (result) {
                alert(result['message'])
            })
            .catch(function (error) {
                alert(error)
            })
    })

    // 创建手工订单
    $('#createNewHandOrder').click(function () {
        var status = []
        var info = true
        var data = {}
        var Form = $("#handOrderForm")
        var inputs = Form.find("input")
        console.log(inputs)
        var VerResult = Verification(...inputs)
        data["saleList"] = []
        if (VerResult.length === 0) {
            var formData = Form.serializeArray();
            $.each(formData, function (index, field) {
                data[field.name] = field.value;
            });
            $("#handOrderTable tr").each(function (index, tr) {
                if (index !== 0) {
                    var a = {}
                    var trId = $(this).data("id").split(splitStr())[0]
                    var trName = $(this).data("id").split(splitStr())[1]
                    var number = $(this).find("input[data-id='number']").val()
                    var price = $(this).find("input[data-id='price']").val()
                    a["sale"] = trId
                    a["name"] = trName
                    a["number"] = number
                    a["price"] = price
                    status = VeriNumm(a)
                    if (status.length !== 0) {
                        alert("数值不能为空")
                        info = false
                        return false;
                    } else {
                        data["saleList"].push(a)
                    }
                }
            })
            if (info) {
                data = JSON.stringify(data)
                var url = '/hand/new'
                JsonRequest(data, url)
                    .then(function (result) {
                        alert(result['message'])
                    })
                    .catch(function (error) {
                        alert(error)
                    })
            }
        }
    })

    // 创建分销订单
    $('#createDisOrder').click(function () {
        var Form = $("#disOrderForm")
        var inputs = Form.find("input")
        console.log(inputs)
        var VerResult = Verification(...inputs)
        if (VerResult.length === 0) {
            var formData = new FormData(document.getElementById("disOrderForm"));
            var file = $('input[name="disOrderFile"]')[0].files[0];
            formData.append('file', file);
            var url = "/hand/disOrder"
            FileRequest(formArray = formData, url = url)
                .then(function (result) {
                    alert(result['message'])
                })
                .catch(function (error) {
                    alert(error)
                })
        }
    })
    $('#uploadPromotionFile').click(function () {
        var formData = new FormData();
        var file = $('input[name="promotionFile"]')[0].files[0];
        formData.append('file', file);
        var url = "/promotion/FilePromotion"
        FileRequest(formArray = formData, url = url)
            .then(function (result) {
                alert(result['message'])
            })
            .catch(function (error) {
                alert(error)
            })
    })
    $('#uploadHandOrderFile').click(function () {
        var formData = new FormData();
        var file = $('input[name="HandOrderFile"]')[0].files[0];
        formData.append('file', file);
        var url = "/back/handOrder"

        FileRequest(formArray = formData, url = url)
            .then(function (result) {
                alert(result['message'])
            })
            .catch(function (error) {
                alert(error)
            })
    })

    $('#uploadCodeConstractFile').click(function () {
        var formData = new FormData();
        var file = $('input[name="codeFile"]')[0].files[0];
        formData.append('file', file);
        var url = "/product/constractCode"
        FileRequest(formArray = formData, url = url)
            .then(function (result) {
                alert(result['message'])
            })
            .catch(function (error) {
                alert(error)
            })
    })

    // 创建权限模型
    $('#createNewPermissionModel').click(function () {
        var Form = $("#newPermissinModelForm")
        var inputs = Form.find("input")
        console.log(inputs)
        var VerResult = Verification(...inputs)
        var url = "/permission/newModel"
        if (VerResult.length === 0) {
            var formData = new FormData(document.getElementById("newPermissinModelForm"));
            FileRequest(formArray = formData, url = url)
                .then(function (result) {
                    alert(result['message'])
                })
                .catch(function (error) {
                    alert(error)
                })
        }
    })

    $('#createNewPermission').click(function () {
        var Form = $("#newPermissionForm")
        var inputs = Form.find("input")
        console.log(inputs)
        var VerResult = Verification(...inputs)
        var url = "/permission/new"
        if (VerResult.length === 0) {
            var formData = new FormData(document.getElementById("newPermissionForm"));
            FileRequest(formArray = formData, url = url)
                .then(function (result) {
                    alert(result['message'])
                })
                .catch(function (error) {
                    alert(error)
                })
        }
    })

    // 新增角色
    $('#createNewRole').click(function () {
        var Form = $("#newRoleForm")
        var formData = Form.serializeArray();
        var inputs = Form.find("input")
        console.log(inputs)
        var VerResult = Verification(inputs)
        var url = "/permission/newRole"
        var data = {}
        data['permission'] = []
        $.each(formData, function (index, field) {
            data[field.name] = field.value;
        });
        if (VerResult.length === 0) {
            inputs = $("#rolePermissionTable").find('input[type="checkbox"]')
            $.each(inputs, function (index, checkbox) {
                if ($(checkbox).is(':checked')) {
                    data['permission'].push($(this).data("id"))
                }
            })
            data = JSON.stringify(data)
            JsonRequest(data, url)
                .then(function (result) {
                    alert(result['message'])
                })
                .catch(function (error) {
                    alert(error)
                })
        }
    })
    // 新增角色
    $('#editRole').click(function () {
        var Form = $("#editRoleForm")
        var formData = Form.serializeArray();
        var inputs = Form.find("input")
        console.log(inputs)
        var VerResult = Verification(inputs)
        var url = "/permission/editRole"
        var data = {}
        data['permission'] = []
        $.each(formData, function (index, field) {
            data[field.name] = field.value;
        });
        if (VerResult.length === 0) {
            inputs = $("#roleEditPermissionTable").find('input[type="checkbox"]')
            $.each(inputs, function (index, checkbox) {
                if ($(checkbox).is(':checked')) {
                    data['permission'].push($(this).data("id"))
                }
            })
            data = JSON.stringify(data)
            JsonRequest(data, url)
                .then(function (result) {
                    alert(result['message'])
                })
                .catch(function (error) {
                    alert(error)
                })
        }
    })

    // 新增用户
    $('#createNewUser').click(function () {
        var Form = $("#newUserForm")
        var inputs = Form.find("input")
        console.log(inputs)
        var VerResult = Verification(...inputs)
        console.log(VerResult)
        if (VerResult.length === 0) {
            var formData = new FormData(document.getElementById("newUserForm"));
            var file = $('input[name="newUserHeadPhoto"]')[0].files[0];
            formData.append('file', file);
            formData.append('remark', $('textarea[data-id="newUserTest"]').val());
            var url = "/user/newUser"
            FileRequest(formArray = formData, url = url)
                .then(function (result) {
                    alert(result['message'])
                })
                .catch(function (error) {
                    alert(error)
                })
        }
    })

    // 登录快递助手
    $('#loginKdzsBtn').click(function () {
        var Form = $("#loginKdzsForm")
        var inputs = Form.find("input")
        console.log(inputs)
        var VerResult = Verification(...inputs)
        var url = "/store/loginKdzs"
        if (VerResult.length === 0) {
            var formData = new FormData(document.getElementById("loginKdzsForm"));
            FileRequest(formArray = formData, url = url)
                .then(function (result) {
                    alert(result['message'])
                })
                .catch(function (error) {
                    alert(error)
                })
        }
    })

    // 获取快递助手订单
    $('#getStoreOrder').click(function () {
        var Form = $("#kdzsOrderForm")
        var inputs = Form.find("input")
        console.log(inputs)
        var VerResult = Verification(...inputs)
        var url = "/store/getStoreOrder"
        if (VerResult.length === 0) {
            var formData = new FormData(document.getElementById("kdzsOrderForm"));
            FileRequest(formArray = formData, url = url)
                .then(function (result) {
                    alert(result['message'])
                })
                .catch(function (error) {
                    alert(error)
                })
        }
    })
    $('#getStoreRefund').click(function () {
        var Form = $("#kdzsOrderForm")
        var inputs = Form.find("input")
        console.log(inputs)
        var VerResult = Verification(...inputs)
        var url = "/store/getStoreRefund"
        if (VerResult.length === 0) {
            var formData = new FormData(document.getElementById("kdzsOrderForm"));
            FileRequest(formArray = formData, url = url)
                .then(function (result) {
                    alert(result['message'])
                })
                .catch(function (error) {
                    alert(error)
                })
        }
    })

    $('#createNewDis').click(function () {
        var Form = $("#newDisForm")
        var inputs = Form.find("input")
        console.log(inputs)
        var VerResult = Verification(...inputs)
        var url = "/store/newDis"
        if (VerResult.length === 0) {
            var formData = new FormData(document.getElementById("newDisForm"));
            formData.append("remark", $('textarea[data-id="newDisText"]').val())
            formData.append("newDisSaleChannel", $('#newDisSaleChannel').val().join(","))
            FileRequest(formArray = formData, url = url)
                .then(function (result) {
                    alert(result['message'])
                })
                .catch(function (error) {
                    alert(error)
                })
        }
    })
    // 登录小红书
    $('#xhsLoginBtn').click(function () {
        var Form = $("#xhsLoginForm")
        var inputs = Form.find("input")
        console.log(inputs)
        var VerResult = Verification(...inputs)
        var url = "/back/loginXhs"
        if (VerResult.length === 0) {
            var formData = new FormData(document.getElementById("xhsLoginForm"));
            FileRequest(formArray = formData, url = url)
                .then(function (result) {
                    alert(result['message'])
                })
                .catch(function (error) {
                    alert(error)
                })
        }
    })

    // 登录小红书
    $('#dyLoginBtn').click(function () {
        var url = "/back/loginDy"
        var formData = new FormData(document.getElementById("dyTestForm"));
        formData.append("name", $('textarea[data-id="dyToken"]').val())
        FileRequest(formArray = formData, url = url)
            .then(function (result) {
                alert(result['message'])
            })
            .catch(function (error) {
                alert(error)
            })
    })

    // 登录快手
    $('#ksLoginBtn').click(function () {
        var Form = $("#ksLoginForm")
        var inputs = Form.find("input")
        var VerResult = Verification(...inputs)
        var url = "/back/loginKs"
        if (VerResult.length === 0) {
            var formData = new FormData(document.getElementById("ksLoginForm"));
            FileRequest(formArray = formData, url = url)
                .then(function (result) {
                    alert(result['message'])
                })
                .catch(function (error) {
                    alert(error)
                })
        }
    })

    // 创建新原料
    $('#createNewAtom').click(function () {
        var Form = $("#newAtomForm")
        var inputs = Form.find("input")
        console.log(inputs)
        var VerResult = Verification(...inputs)
        var url = "/product/newAtom"
        if (VerResult.length === 0) {
            var formData = new FormData(document.getElementById("newAtomForm"));
            formData.append("remark", $('textarea[data-id="new-atom"]').val())
            FileRequest(formArray = formData, url = url)
                .then(function (result) {
                    alert(result['message'])
                })
                .catch(function (error) {
                    alert(error)
                })
        }
    })

    // 创建新供应商
    $('#createNewSupplier').click(function () {
        var Form = $("#newSupplierForm")
        var inputs = Form.find("input")
        console.log(inputs)
        var VerResult = Verification(...inputs)
        var url = "/product/newSupplier"
        if (VerResult.length === 0) {
            var formData = new FormData(document.getElementById("newSupplierForm"));
            formData.append("remark", $('textarea[data-id="newSupplierText"]').val())
            FileRequest(formArray = formData, url = url)
                .then(function (result) {
                    alert(result['message'])
                })
                .catch(function (error) {
                    alert(error)
                })
        }
    })

    // 创建采购单
    $('#createNewPurchase').click(function () {
        var data = {}
        data["purchaseList"] = []
        var Form = $("#newPurchaseForm")
        var inputs = Form.find("input")
        var formData = Form.serializeArray();
        $.each(formData, function (index, field) {
            data[field.name] = field.value;
        });
        data['remark'] = $("textarea[data-id='newPurchaseText']").val()
        data['totalCost'] = $("#total-pr-price").text()
        var VerResult = Verification(...inputs)
        if (VerResult.length === 0) {
            $("#purchaseListTable tr").each(function (index, tr) {
                if (index !== 0) {
                    var a = {}
                    a["atomId"] = $(tr).find('td:eq(0)').find("small").data("id")
                    a["atom"] = $(tr).find('td:eq(0)').find("small").text()
                    a["supplierId"] = $(tr).find('td:eq(1)').find("small").data("id")
                    a["supplier"] = $(tr).find('td:eq(1)').find("small").text()
                    a["number"] = $(tr).find('td:eq(2)').find("small").text()
                    a["unitPrice"] = $(tr).find('td:eq(3)').find("small").text()
                    a["TotalPrice"] = $(tr).find('td:eq(4)').find("small").text()
                    data["purchaseList"].push(a)
                }
            })
            data = JSON.stringify(data)
            var url = '/product/newPurchase'
            JsonRequest(data, url)
                .then(function (result) {
                    alert(result['message'])
                })
                .catch(function (error) {
                    alert(error)
                })
        }
    })
})

// 增加销售商品项
$('#createNewSale').click(function () {
    var data = {}
    data['atomlist'] = []
    var status = []
    var info = true
    var Form = $("#newSaleForm")
    var inputs = Form.find("input")
    var formData = Form.serializeArray();
    $.each(formData, function (index, field) {
        data[field.name] = field.value;
    });
    console.log(inputs)
    var VerResult = Verification(...inputs)
    if (VerResult.length === 0) {
        $("#createNewSaleTable tr").each(function (index, tr) {
            if (index !== 0) {
                var a = {}
                a["atomCode"] = $(tr).data("id")
                a["number"] = $(tr).find('input[type="number"]').val()
                status = VeriNumm(a)
                if (status.length !== 0) {
                    alert("数值不能为空")
                    info = false
                    return false;
                } else {
                    data["atomlist"].push(a)
                }
            }
        })
        if (info) {
            data = JSON.stringify(data)
            var url = '/product/newSaleProduct'
            JsonRequest(data, url)
                .then(function (result) {
                    alert(result['message'])
                })
                .catch(function (error) {
                    alert(error)
                })
        }
    }
})

// 增加组合商品项
$('#createNewGruop').click(function () {
    var data = {}
    data['saleList'] = []
    var status = []
    var info = true
    var Form = $("#newGroupForm")
    var inputs = Form.find("input")
    var formData = Form.serializeArray();
    $.each(formData, function (index, field) {
        data[field.name] = field.value;
    });
    console.log(inputs)
    var VerResult = Verification(...inputs)
    if (VerResult.length === 0) {
        $("#newGroupTable tr").each(function (index, tr) {
            if (index !== 0) {
                var a = {}
                a["saleCode"] = $(tr).data("id")
                status = VeriNumm(a)
                if (status.length !== 0) {
                    alert("不能为空")
                    info = false
                    return false;
                } else {
                    data["saleList"].push(a)
                }

            }
        })
        data = JSON.stringify(data)
        if (info) {
            var url = '/product/newGroupProduct'
            JsonRequest(data, url)
                .then(function (result) {
                    alert(result['message'])
                })
                .catch(function (error) {
                    alert(error)
                })
        }
    }
})

$('#newStorePro').click(function () {
    var Form = $("#newStoreProForm")
    var inputs = Form.find("input")
    console.log(inputs)
    var VerResult = Verification(...inputs)
    var url = "/store/newStorePro"
    if (VerResult.length === 0) {
        var formData = new FormData(document.getElementById("newStoreProForm"));
        FileRequest(formArray = formData, url = url)
            .then(function (result) {
                alert(result['message'])
            })
            .catch(function (error) {
                alert(error)
            })
    }
})


$(".newSelectBtn").click(function () {
    var Link = $(this).data("id")
    var Form = $(this).closest(".border-bottom").find("form")
    var FormId = $(Form).attr("id")
    var inputs = Form.find("input")
    var VerResult = Verification(...inputs)
    var url = "/back/" + Link
    console.log(FormId, url)
    if (VerResult.length === 0) {
        var formData = new FormData(document.getElementById(FormId));
        FileRequest(formArray = formData, url = url)
            .then(function (result) {
                alert(result['message'])
            })
            .catch(function (error) {
                alert(error)
            })
    }
})

$("#getHandOrder").click(function () {
    var formData = new FormData(document.getElementById("searchHandOrderForm"));
    var url = "/hand/order"
    FileRequest(formArray = formData, url = url)
})