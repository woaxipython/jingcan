import math

from APP.SQLAPP.addEdit.orderStore import writeOrderData
from APP.Spyder.KdzsSpyder import KuaiDiZhuShouSpyder

kdzs = KuaiDiZhuShouSpyder()
def getOrder(stores, endDate, startDate, token):
    order_JSON = kdzs.getOrder(stores, endDate=endDate, startDate=startDate, token=token)
    totalCount = int(order_JSON['total'])
    pageNo = math.ceil(totalCount / 1000)
    dealResults = kdzs.DealOrder(order_JSON=order_JSON)
    i = 1
    status = {"total": totalCount, "processed": 0}
    for dealresult in dealResults:
        writeOrderData(dealresult)
        i += 1
        status["processed"] = i
        print("共计{}条订单，已更新至第{}条,剩余{}条".format(totalCount, i, totalCount - i))
    for page in range(2, pageNo + 1):
        order_JSON = kdzs.getOrder(pageNo=page, stores=stores, endDate=endDate, startDate=startDate, token=token)
        dealResults = kdzs.DealOrder(order_JSON=order_JSON)
        for dealresult in dealResults:
            print(i)
            writeOrderData(dealresult)
            status["processed"] = i
            i += 1
            print("共计{}条订单，已更新至第{}条,剩余{}条".format(totalCount, i, totalCount - i))
        time.sleep(80)
    return status
