def createAtomCode(brand, category, max_id):
    barnd_id = 10 + int(brand)
    category_id = 10 + int(category)
    max_id = 100 + int(max_id)
    return str(barnd_id) + str(category_id) + str(max_id)


def createSaleCode(max_id):
    Int = 100000 + max_id
    SaleId = "Z" + str(Int)
    return SaleId


def createGroupCode(max_id):
    Int = 100000 + max_id
    GroupId = "G" + str(Int)
    print(GroupId)
    return GroupId


def createOrderCode(max_id):
    Int = 100000 + max_id
    OrderId = "O" + str(Int)
    return OrderId

def createDisOrderCode(max_id):
    Int = 100000 + max_id
    OrderId = "D" + str(Int)
    return OrderId


if __name__ == '__main__':
    Pr = CodeCreate()
    Pr.createGroupCode(1)
