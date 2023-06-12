import jsonschema
from jsonschema import validate


class newGroupForm():
    def __init__(self, data):
        self.schema = {
            "type": "object",
            "properties": {
                "newGroupName": {"type": "string", "minLength": 4, "maxLength": 10},
                "saleList": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "saleCode':": {"type": "integer", "pattern": "^[0-9]+$"},
                        },
                        "required": ["saleCode"]
                    }
                },
            },
            "required": ["newGroupName", "saleList"]
        }
        self.data = data
        self.messages = []

    def validate(self):
        try:
            validate(instance=self.data, schema=self.schema)
            return True
        except jsonschema.exceptions.ValidationError as e:
            self.messages.append(str(e).split("\n")[0])
            return False


class newSaleForm():
    def __init__(self, data):
        self.schema = {
            "type": "object",
            "properties": {
                "newSaleName": {"type": "string", "minLength": 4, "maxLength": 20},
                "newSaleSkuName": {"type": "string", "minLength": 4, "maxLength": 40},
                "newSalePrice": {"type": "string", "pattern": "^[0-9]+(\.[0-9]+)?$"},
                "atomlist": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "atomCode':": {"type": "integer", "pattern": "^[0-9]+$"},
                            "number": {"type": "string", "maxLength": 10},
                        },
                        "required": ["atomCode", "number"]
                    }
                },
            },
            "required": ["newSaleName", "newSaleSkuName", "atomlist"]
        }
        self.data = data
        self.messages = []

    def validate(self):
        try:
            validate(instance=self.data, schema=self.schema)
            return True
        except jsonschema.exceptions.ValidationError as e:
            self.messages.append(str(e).split("\n")[0])
            return False


class newPurchaseForm():
    def __init__(self, data):
        self.schema = {
            "type": "object",
            "properties": {
                "newPurchaseUser": {"type": "string", "pattern": "^[0-9]+$"},
                "newPurchaseName": {"type": "string", "maxLength": 50},
                "newPurchaseOther": {"type": "string", "pattern": "^[0-9]+(\.[0-9]+)?$"},
                "newPurchaseFreight": {"type": "string", "pattern": "^[0-9]+(\.[0-9]+)?$"},
                "remark": {"type": "string", "maxLength": 100},
                "totalCost": {"type": "string", "pattern": "^[0-9]+(\.[0-9]+)?$"},
                "purchaseList": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "atomId": {"type": "integer", "pattern": "^[0-9]+$"},
                            "atom": {"type": "string", "maxLength": 10},
                            "supplierId": {"type": "integer", "pattern": "^[0-9]+$"},
                            "supplier": {"type": "string", "maxLength": 10},
                            "number": {"type": "string", "pattern": "^[0-9]+$"},
                            "unitPrice": {"type": "string", "pattern": "^[0-9]+(\.[0-9]+)?$"},
                            "TotalPrice": {"type": "string", "pattern": "^[0-9]+(\.[0-9]+)?$"},
                        },
                        "required": ["atomId", "atom", "supplierId", "supplier", "number", "unitPrice", "TotalPrice"]
                    }
                },
            },
            "required": ["newPurchaseUser", "newPurchaseName", "newPurchaseOther", "newPurchaseFreight",
                         "totalCost", "purchaseList"]
        }
        self.data = data
        self.messages = []

    def validate(self):
        try:
            validate(instance=self.data, schema=self.schema)
            return True
        except jsonschema.exceptions.ValidationError as e:
            self.messages.append(str(e).split("\n")[0])
            return False


class StoreProForm():
    def __init__(self, data):
        self.schema = {
            "type": "object",
            "properties": {
                "Adist": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "plat": {"type": "string", "pattern": "^[0-9]+$"},
                            "method": {"type": "string", "pattern": "^[0-9]+$"},
                            "store": {"type": "string", "pattern": "^[0-9]+$"},
                            "product": {"type": "string", "pattern": "^[0-9]+$"},
                            "fee": {"type": "string", "pattern": "^[0-9]+(\.[0-9]+)?$"},
                            "date": {"type": "string", "pattern": "^^\d{4}-\d{2}-\d{2}$"}
                        },
                        "required": ["plat", "method", "store", "product", "number", "date"]
                    }
                }
            },
        }
        self.data = data
        self.messages = []

    def validate(self):
        try:
            validate(instance=self.data, schema=self.schema)
            return True
        except jsonschema.exceptions.ValidationError as e:
            self.messages.append(str(e).split("\n")[0])
            return False


class NewPromotionForm():
    def __init__(self, data):
        self.schema = {
            "type": "object",
            "properties": {
                "promotionWechat": {"type": "string", "maxLength": 30},
                "promotionUser": {"type": "string", "pattern": "^[0-9]+$"},
                "promotionRate": {"type": "string", "pattern": "^[0-9]+$"},
                "promotionFeeModel": {"type": "string", "pattern": "^[0-9]+$"},
                "promotionFee": {"type": "string", "pattern": "^[0-9]+(\.[0-9]+)?$"},
                "promotionCommission": {"type": "string", "pattern": "^[0-9]+(\.[0-9]+)?$"},
                "PromotionCheck": {"type": "string", "pattern": "^[0-9]+$"},
                "promotionOrder": {"type": "string", "maxLength": 50},
                "AccountList": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "plat": {"type": "string", "pattern": "^[0-9]+$"},
                            "account": {"type": "string", "maxLength": 50},
                        },
                        "required": ["plat", "account"]
                    }
                },
                "promotionPr": {
                    "type": "array",
                    "items": {"type": "string", "pattern": "^[0-9]+$"}
                }
            },
            "required": ["promotionWechat", "promotionUser", "promotionRate", "promotionFeeModel"]

        }
        self.data = data
        self.messages = []

    def validate(self):
        try:
            validate(instance=self.data, schema=self.schema)
            return True
        except jsonschema.exceptions.ValidationError as e:
            self.messages.append(str(e).split("\n")[0])
            return False

class GetPromotionForm():
    def __init__(self, data):
        self.schema = {
            "type": "object",
            "properties": {
                "rate": {"type": "string", "pattern": "^[0-9]+$"},
                "user": {"type": "string", "pattern": "^[0-9]+$"},
                "start_date": {"type": "string", "pattern": "^[0-9]{4}-[0-9]{2}-[0-9]{2}$"},
                "end_date": {"type": "string", "pattern": "^[0-9]{4}-[0-9]{2}-[0-9]{2}$"},
            },
            "required": []

        }
        self.data = data
        self.messages = []

    def validate(self):
        try:
            validate(instance=self.data, schema=self.schema)
            return True
        except jsonschema.exceptions.ValidationError as e:
            self.messages.append(str(e).split("\n")[0])
            return False


class ProfileLinkForm():
    def __init__(self, data):

        self.schema = {
            "type": "object",
            "properties": {
                "profileLink": {"type": "string",
                                "pattern": "^(http|https):\/\/[a-zA-Z0-9\-\.]+\.[a-zA-Z]{2,}(\/\S*)?$"},
                "platId": {"type": "string", "pattern": "^[0-9]+$"},
            },
            "required": ["profileLink", "platId"]
        }
        self.data = data
        self.messages = []

    def validate(self):
        try:
            validate(instance=self.data, schema=self.schema)
            return True
        except jsonschema.exceptions.ValidationError as e:
            self.messages.append(str(e).split("\n")[0])
            return False


class NotesLinkForm():
    def __init__(self, data):

        self.schema = {
            "type": "object",
            "properties": {
                "noteLink": {"type": "string",
                             "pattern": "^(http|https):\/\/[a-zA-Z0-9\-\.]+\.[a-zA-Z]{2,}(\/\S*)?$"},
                "promotion_id": {"type": "string", "pattern": "^[0-9]+$"},
                "account_id": {"type": "string", "maxLength": 80},
                "note_id": {"type": "string", "pattern": "^[0-9]+$"},
            },
            "required": ["noteLink", "promotion_id", "account_id", "note_id"]
        }
        self.data = data
        self.messages = []

    def validate(self):
        try:
            validate(instance=self.data, schema=self.schema)
            return True
        except jsonschema.exceptions.ValidationError as e:
            self.messages.append(str(e).split("\n")[0])
            return False


class EditPromotionForm():
    def __init__(self, data):

        self.schema = {
            "type": "object",
            "properties": {
                "editPromotionOrderId": {"type": "string", "maxLength": 50},
                "editPromotionCheck": {"type": "string", "pattern": "^(0|1)?$"},
                "editPromotionId": {"type": "string", "pattern": "^[0-9]+$"},
            },
            "required": ["editPromotionId"]
        }
        self.data = data
        self.messages = []

    def validate(self):
        try:
            validate(instance=self.data, schema=self.schema)
            return True
        except jsonschema.exceptions.ValidationError as e:
            self.messages.append(str(e).split("\n")[0])
            return False


class NewHandOrderForm():
    def __init__(self, data):
        self.schema = {
            "type": "object",
            "properties": {
                "handOrderUser": {"type": "string", "pattern": "^[0-9]+$"},
                "handOrderModel": {"type": "string", "pattern": "^[0-9]+$"},
                "handOrderRemark": {"type": "string", "maxLength": 50},
                "handOrderName": {"type": "string", "maxLength": 20},
                "handOrderPhone": {"type": "string", "maxLength": 30},
                "handOrderCity": {"type": "string", "maxLength": 20},
                "handOrderProvince": {"type": "string", "maxLength": 20},
                "handOrderAddress": {"type": "string", "maxLength": 100},
                "saleList": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "sale": {"type": "string", "maxLength": 80},
                            "number": {"type": "string", "pattern": "^[0-9]+$"},
                            "price": {"type": "string", "pattern": "^[1-9]+(\.[0-9])?$|0"},
                        },
                        "required": ["sale", "number", "price"]
                    }
                },
            },
            "required": ["handOrderUser", "handOrderModel", "handOrderName",
                         "handOrderPhone", "handOrderCity", "handOrderProvince", "handOrderAddress"]

        }
        self.data = data
        self.messages = []

    def validate(self):
        try:
            validate(instance=self.data, schema=self.schema)
            return True
        except jsonschema.exceptions.ValidationError as e:
            self.messages.append(str(e).split("\n")[0])
            return False


class PermissionModelForm():
    def __init__(self, data):

        self.schema = {
            "type": "object",
            "properties": {
                "newPermissinModel": {"type": "string", "minLength": 2, "maxLength": 6},
            },
            "required": ["newPermissinModel"]
        }
        self.data = data
        self.messages = []

    def validate(self):
        try:
            validate(instance=self.data, schema=self.schema)
            return True
        except jsonschema.exceptions.ValidationError as e:
            self.messages.append(str(e).split("\n")[0])
            return False


class PermissionForm():
    def __init__(self, data):

        self.schema = {
            "type": "object",
            "properties": {
                "permissionModel": {"type": "string", "pattern": "^[0-9]+$"},
                "newPermissionName": {"type": "string", "minLength": 2, "maxLength": 6},
            },
            "required": ["permissionModel", "newPermissionName"]
        }
        self.data = data
        self.messages = []

    def validate(self):
        try:
            validate(instance=self.data, schema=self.schema)
            return True
        except jsonschema.exceptions.ValidationError as e:
            self.messages.append(str(e).split("\n")[0])
            return False


class RoleForm():
    def __init__(self, data):
        self.schema = {
            "type": "object",
            "properties": {
                "newRoleName": {"type": "string", "minLength": 2, "maxLength": 6},
                "newRoleDesc": {"type": "string", "minLength": 2, "maxLength": 50},
                "permission": {
                    "type": "array",
                    "items": {"type": "integer", }
                }
            },
            "required": ["newRoleName", "permission", ]

        }
        self.data = data
        self.messages = []

    def validate(self):
        try:
            validate(instance=self.data, schema=self.schema)
            return True
        except jsonschema.exceptions.ValidationError as e:
            self.messages.append(str(e).split("\n")[0])
            return False


class EditRoleForm():
    def __init__(self, data):
        self.schema = {
            "type": "object",
            "properties": {
                "editRoleId": {"type": "string", "pattern": "^[0-9]+$"},
                "permission": {
                    "type": "array",
                    "items": {"type": "integer", }
                }
            },
            "required": ["editRoleId", "permission", ]

        }
        self.data = data
        self.messages = []

    def validate(self):
        try:
            validate(instance=self.data, schema=self.schema)
            return True
        except jsonschema.exceptions.ValidationError as e:
            self.messages.append(str(e).split("\n")[0])
            return False


class UserForm():
    def __init__(self, data):
        self.schema = {
            "type": "object",
            "properties": {
                "newUserName": {"type": "string", "minLength": 2, "maxLength": 10},
                "newUserPhone": {"type": "string", "minLength": 11, "maxLength": 20},
                "newUserCity": {"type": "string", "minLength": 2, "maxLength": 15},
                "newUserProvince": {"type": "string", "minLength": 2, "maxLength": 20},
                "newUserCards": {"type": "string", "minLength": 18, "maxLength": 18},
                "newUserAddress": {"type": "string", "minLength": 10, "maxLength": 100},
                "newUserDegree": {"type": "string", "minLength": 2, "maxLength": 20},
                "newUserUniversity": {"type": "string", "minLength": 2, "maxLength": 20},
                "newUserCost": {"type": "string", "pattern": "^[0-9]+$"},
                "newUserEmail": {"type": "string", "pattern": "^[a-zA-Z0-9_-]+@[a-zA-Z0-9_-]+(.[a-zA-Z0-9_-]+)+$"},
                "newUserGender": {"type": "string", "pattern": "0|1"},
                "newUserPassword": {"type": "string", "minLength": 2, "maxLength": 15},
                "newUserRole": {"type": "string", "pattern": "^[0-9]+$"},
                "newUserWechat": {"type": "string", "minLength": 2, "maxLength": 30},
                "remark": {"type": "string", "maxLength": 100},
            },
            "required": ["newUserName", "newUserPhone", "newUserCity", "newUserProvince", "newUserCards",
                         "newUserAddress", "newUserDegree", "newUserCost", "newUserEmail",
                         "newUserGender", "newUserPassword", "newUserRole", "newUserWechat", ]
        }
        self.data = data
        self.messages = []

    def validate(self):
        try:
            validate(instance=self.data, schema=self.schema)
            return True
        except jsonschema.exceptions.ValidationError as e:
            self.messages.append(str(e).split("\n")[0])
            return False


class KdzsLoginForm():
    def __init__(self, data):
        self.schema = {
            "type": "object",
            "properties": {
                "kdzsAccount": {"type": "string", "minLength": 2, "maxLength": 15},
                "kdzsPassword": {"type": "string", "minLength": 2, "maxLength": 20},
                "kdzsCaptcha": {"type": "string", "minLength": 4, "maxLength": 4},
                "kdzsPhoneCode": {"type": "string", "pattern": "^(|\d+)$", "maxLength": 6},
            },
            "required": ["kdzsAccount", "kdzsPassword", "kdzsCaptcha"]
        }
        self.data = data
        self.messages = []

    def validate(self):
        try:
            validate(instance=self.data, schema=self.schema)
            return True
        except jsonschema.exceptions.ValidationError as e:
            self.messages.append(str(e).split("\n")[0])
            return False


class OrderForm():
    def __init__(self, data):
        self.schema = {
            "type": "object",
            "properties": {
                "kdzsStartDate": {"type": "string", "pattern": "^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}$"},
                "kdzsEndDate": {"type": "string", "pattern": "^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}$"},
                "kdzsStore": {"type": "string", "pattern": "^All|[0-9]+$"},
                "kdzsPhoneCode": {"type": "string", "pattern": "^[0-9]+$"},
            },
            "required": ["kdzsStartDate", "kdzsEndDate", "kdzsStore"]
        }
        self.data = data
        self.messages = []

    def validate(self):
        try:
            validate(instance=self.data, schema=self.schema)
            return True
        except jsonschema.exceptions.ValidationError as e:
            self.messages.append(str(e).split("\n")[0])
            return False


class KsLoginForm():
    def __init__(self, data):
        self.schema = {
            "type": "object",
            "properties": {
                "ksAccount": {"type": "string", "minLength": 2, "maxLength": 15},
                "ksPhoneCode": {"type": "string", "minLength": 2, "maxLength": 20},
            },
            "required": ["ksAccount", "ksPhoneCode"]
        }
        self.data = data
        self.messages = []

    def validate(self):
        try:
            validate(instance=self.data, schema=self.schema)
            return True
        except jsonschema.exceptions.ValidationError as e:
            self.messages.append(str(e).split("\n")[0])
            return False


class XhsForm():
    def __init__(self, data):
        self.schema = {
            "type": "object",
            "properties": {
                "xhsToken": {"type": "string", "minLength": 41, "maxLength": 41},
                "xhsWechat": {"type": "string", "minLength": 2, "maxLength": 100},
                "xhsPhone": {"type": "string", "minLength": 2, "maxLength": 100},
            },
            "required": ["xhsToken"]
        }
        self.data = data
        self.messages = []

    def validate(self):
        try:
            validate(instance=self.data, schema=self.schema)
            return True
        except jsonschema.exceptions.ValidationError as e:
            self.messages.append(str(e).split("\n")[0])
            return False


class DyForm():
    def __init__(self, data):
        self.schema = {
            "type": "object",
            "properties": {
                "name": {"type": "string", "minLength": 200, "maxLength": 5000},
            },
            "required": ["name"]
        }
        self.data = data
        self.messages = []

    def validate(self):
        try:
            validate(instance=self.data, schema=self.schema)
            return True
        except jsonschema.exceptions.ValidationError as e:
            self.messages.append(str(e).split("\n")[0])
            return False


class SearchAtomForm():
    def __init__(self, data):
        self.schema = {
            "type": "object",
            "properties": {
                "searchAtomName": {"type": "string", "minLength": 2, "maxLength": 10},
            },
            "required": ["searchAtomName"]
        }
        self.data = data
        self.messages = []
class AtomForm():
    def __init__(self, data):
        self.schema = {
            "type": "object",
            "properties": {
                "newAtomCode": {"type": "string", "maxLength": 6},
                "newAtomName": {"type": "string", "minLength": 2, "maxLength": 10},
                "newAtomCategory": {"type": "string", "pattern": "^[0-9]+$"},
                "newAtomWeight": {"type": "string", "pattern": "^[0-9]+(\.[0-9]+)?$"},
                "newAtomUnit": {"type": "string", "pattern": "^[0-9]+$"},
                "newAtomSupplier": {"type": "string", "pattern": "^[0-9]+$"},
                "newAtomBrand": {"type": "string", "pattern": "^[0-9]+$"},
                "remark": {"type": "string", "maxLength": 100},
            },
            "required": ["newAtomName", "newAtomCategory", "newAtomWeight", "newAtomUnit", "newAtomSupplier",
                         "newAtomBrand"]
        }
        self.data = data
        self.messages = []

    def validate(self):
        try:
            validate(instance=self.data, schema=self.schema)
            return True
        except jsonschema.exceptions.ValidationError as e:
            self.messages.append(str(e).split("\n")[0])
            return False


class SupplierForm():
    def __init__(self, data):
        self.schema = {
            "type": "object",
            "properties": {
                "newSupplierCampany": {"type": "string", "minLength": 4, "maxLength": 40},
                "newSupplierSimpleName": {"type": "string", "minLength": 2, "maxLength": 20},
                "newSupplierName": {"type": "string", "minLength": 2, "maxLength": 6},
                "newSupplierGender": {"type": "string", "pattern": "0|1"},
                "newSupplierAge": {"type": "string", "maxLength": 100},
                "newSupplierPhone": {"type": "string", "pattern": "^[0-9]+$", "minLength": 11, "maxLength": 11},
                "newSupplierWechat": {"type": "string", "maxLength": 50},
                "newSupplierCity": {"type": "string", "minLength": 2, "maxLength": 15},
                "newSupplierProvince": {"type": "string", "minLength": 2, "maxLength": 15},
                "newSupplierAddress": {"type": "string", "minLength": 2, "maxLength": 50},
                "newSupplierUser": {"type": "string", "pattern": "^[0-9]+$"},
                "remark": {"type": "string", "maxLength": 100},
            },
            "required": ["newSupplierCampany", "newSupplierName", "newSupplierGender", "newSupplierWechat",
                         "newSupplierSimpleName", "newSupplierPhone", "newSupplierCity",
                         "newSupplierProvince", "newSupplierAddress", "newSupplierUser"]
        }
        self.data = data
        self.messages = []

    def validate(self):
        try:
            validate(instance=self.data, schema=self.schema)
            return True
        except jsonschema.exceptions.ValidationError as e:
            self.messages.append(str(e).split("\n")[0])
            return False


class DisForm():
    def __init__(self, data):
        self.schema = {
            "type": "object",
            "properties": {
                "newDisCampany": {"type": "string", "minLength": 4, "maxLength": 30},
                "newDisName": {"type": "string", "minLength": 2, "maxLength": 6},
                "newDisPhone": {"type": "string", "pattern": "^[0-9]+$", "minLength": 11, "maxLength": 11},
                "newDisWechat": {"type": "string", "minLength": 2, "maxLength": 50},
                "newDisSaleChannel": {"type": "string", "minLength": 2, "maxLength": 50},
                "newDisCity": {"type": "string", "minLength": 2, "maxLength": 15},
                "newDisProvince": {"type": "string", "minLength": 2, "maxLength": 15},
                "newDisAddress": {"type": "string", "minLength": 2, "maxLength": 50},
                "newDisLink": {"type": "string", },
                "newDisUser": {"type": "string", "pattern": "^[0-9]+$"},
                "remark": {"type": "string", "maxLength": 100},
            },
            "required": ["newDisCampany", "newDisName", "newDisPhone", "newDisCity",
                         "newDisProvince", "newDisAddress", "newDisUser", "newDisWechat", "newDisSaleChannel"]
        }
        self.data = data
        self.messages = []

    def validate(self):
        try:
            validate(instance=self.data, schema=self.schema)
            return True
        except jsonschema.exceptions.ValidationError as e:
            self.messages.append(str(e).split("\n")[0])
            return False


class newStoreProForm():
    def __init__(self, data):
        self.schema = {
            "type": "object",
            "properties": {
                "platName": {"type": "string", "pattern": "^[0-9]+$"},
                "proName": {"type": "string", "minLength": 2, "maxLength": 10},
                "proFeeModel": {"type": "string", "minLength": 2, "maxLength": 10},
            },
            "required": ["platName", "proName", "proFeeModel"]
        }
        self.data = data
        self.messages = []

    def validate(self):
        try:
            validate(instance=self.data, schema=self.schema)
            return True
        except jsonschema.exceptions.ValidationError as e:
            self.messages.append(str(e).split("\n")[0])
            return False
