from datetime import datetime

import xlrd
from openpyxl.reader.excel import load_workbook


class StoreProFile():
    def __init__(self, save_path):
        self.save_path = save_path
        self.messages = []
        if "xlsx" in self.save_path:
            self.validate_xlsx()
        elif "xls" in self.save_path:
            self.validate_xls()

    def validate_xls(self):
        workbook = xlrd.open_workbook(self.save_path)
        sheet = workbook.sheet_by_index(0)
        if sheet.nrows == 0:
            self.messages.append('表格数据不能为空')
            return False
        elif sheet.ncols != 6:
            self.messages.append('表格标头不正确，请下载模板')
            return False
        elif sheet.cell(0, 0).value != '推广平台' or sheet.cell(0, 1).value != '推广方式' or sheet.cell(0,
                                                                                                        2).value != '推广店铺' \
                or sheet.cell(0, 3).value != '推广产品' or sheet.cell(0, 4).value != '推广花费' or sheet.cell(0,
                                                                                                              5).value != '推广时间':
            self.messages.append('表格列名不正确')
            return False
        else:
            for row in range(1, sheet.nrows):
                if not sheet.cell(row, 0).value or not sheet.cell(row, 1).value or not sheet.cell(row, 2).value or not \
                        sheet.cell(row, 3).value or not sheet.cell(row, 4).value or not sheet.cell(row, 5).value:
                    self.messages.append('表格数据不能为空')
                    break
            for row in range(1, sheet.nrows):
                if not isinstance(sheet.cell(row, 4).value, float):
                    self.messages.append('推广花费应当是数字')
                    break
            for row in range(1, sheet.nrows):
                if not isinstance(sheet.cell(row, 5).value, datetime):
                    self.messages.append('推广时间应当是日期')
                    break
            for row in range(1, sheet.nrows):
                if not isinstance(sheet.cell(row, 2).value, str):
                    self.messages.append('推广店铺应当是字符串')
                    break
            for row in range(1, sheet.nrows):
                if not isinstance(sheet.cell(row, 3).value, str):
                    self.messages.append('推广产品应当是字符串')
                    break
            for row in range(1, sheet.nrows):
                if not isinstance(sheet.cell(row, 0).value, str):
                    self.messages.append('推广平台应当是字符串')
                    break
            for row in range(1, sheet.nrows):
                if not isinstance(sheet.cell(row, 1).value, str):
                    self.messages.append('推广方式应当是字符串')
                    break

    def validate_xlsx(self):
        workbook = load_workbook(filename=self.save_path)
        sheet = workbook.active

        header = ['推广平台', '推广方式', '推广店铺', '推广产品', '推广花费', '推广时间', ]
        head_row = sheet[1]
        for cell in head_row:
            if cell.value != header[head_row.index(cell)]:
                self.messages.append('表头错误')
                break
        for row in sheet.iter_rows(min_row=2):
            if not row[0].value or not row[1].value or not row[2].value or not row[3].value or not row[4].value or not \
                    row[5].value:
                self.messages.append('表格数据错误')
                break
        for row in sheet.iter_rows(min_row=2):
            if not isinstance(row[4].value, int):
                self.messages.append('推广花费应当是数字')
                break
        for row in sheet.iter_rows(min_row=2):
            if not isinstance(row[5].value, datetime):
                self.messages.append('推广时间应当是日期')
                break

        for row in sheet.iter_rows(min_row=2):
            if not isinstance(row[2].value, str):
                self.messages.append('推广店铺应当是字符串')
                break

        for row in sheet.iter_rows(min_row=2):
            if not isinstance(row[3].value, str):
                self.messages.append('推广产品应当是字符串')
                break

        for row in sheet.iter_rows(min_row=2):
            if not isinstance(row[1].value, str):
                self.messages.append('推广方式应当是字符串')
                break
        for row in sheet.iter_rows(min_row=2):
            if not isinstance(row[0].value, str):
                self.messages.append('推广平台应当是字符串')
                break

    def validate(self):
        if self.messages:
            return False
        else:
            return True


class HandOrderFile():
    def __init__(self, save_path):
        self.save_path = save_path
        self.messages = []
        self.validate_xlsx()

    def validate_xlsx(self):
        workbook = load_workbook(filename=self.save_path)
        try:
            sheet = workbook['分销商订单模板']
        except:
            self.messages.append('表格名称不正确，请下载模板')
            return False

        header = ["商品名称", "商品数量", "商品单价", "收件人", "收件人电话", "收件人地址"]
        head_row = sheet[1]
        for cell in head_row:
            if cell.value != header[head_row.index(cell)]:
                self.messages.append('表头错误')
                break
        for row in sheet.iter_rows(min_row=2):
            if not row[0].value or not row[1].value or not row[2].value or not row[3].value or not row[4].value or not \
                    row[5].value:
                self.messages.append('表格数据不能为空')
        for row in sheet.iter_rows(min_row=2):
            if not isinstance(row[0].value, str):
                self.messages.append('第{}行第{}列商品名称应当是字符串'.format(row[0].row, row[0].column))
                return False
        for row in sheet.iter_rows(min_row=2):
            if not isinstance(row[1].value, int):
                self.messages.append('第{}行第{}列数量应当是整数数字'.format(row[1].row, row[1].column))
                return False
        for row in sheet.iter_rows(min_row=2):
            if not isinstance(row[2].value, float) and not isinstance(row[2].value, int):
                self.messages.append('第{}行第{}列单价应当是数字'.format(row[2].row, row[2].column))
                return False
        for row in sheet.iter_rows(min_row=2):
            if not isinstance(row[3].value, str):
                self.messages.append('第{}行第{}列收件人应当是字符串'.format(row[3].row, row[3].column))
                return False
        for row in sheet.iter_rows(min_row=2):
            if not isinstance(row[4].value, str) and not isinstance(row[4].value, int):
                self.messages.append('第{}行第{}列收件人电话应当是字符串或数字'.format(row[4].row, row[4].column))
                return False
        for row in sheet.iter_rows(min_row=2):
            if not isinstance(row[5].value, str):
                self.messages.append('第{}行第{}列收件人地址应当是字符串'.format(row[5].row, row[5].column))
                return False

    def validate(self):
        if self.messages:
            return False
        else:
            return True


class codeContractFileForm():
    def __init__(self, save_path):
        self.save_path = save_path
        self.messages = []
        self.validate_xlsx()

    def validate_xlsx(self):
        workbook = load_workbook(filename=self.save_path)
        try:
            sheet = workbook.active
        except:
            self.messages.append('表格名称不正确，请下载模板')
            return False
        header = ["销售名称", "商品编码"]
        head_row = sheet[1]
        for cell in head_row:
            if cell.value != header[head_row.index(cell)]:
                self.messages.append('表头错误')
                break
        for row in sheet.iter_rows(min_row=2):
            if not row[0].value or not row[1].value:
                self.messages.append('表格数据不能为空')
        for row in sheet.iter_rows(min_row=2):
            if not isinstance(row[0].value, str):
                self.messages.append('第{}行第{}列销售名称应当是字符串'.format(row[0].row, row[0].column))
                return False
        for row in sheet.iter_rows(min_row=2):
            if not isinstance(row[1].value, str):
                self.messages.append('第{}行第{}列商品编码应当是字符串'.format(row[1].row, row[1].column))
                return False

    def validate(self):
        if self.messages:
            return False
        else:
            return True


class PromotionFileForm():
    def __init__(self, save_path):
        self.save_path = save_path
        self.messages = []
        self.validate_xlsx()

    def validate_xlsx(self):
        workbook = load_workbook(filename=self.save_path)
        try:
            sheet = workbook.active
        except:
            self.messages.append('表格名称不正确，请下载模板')
            return False
        header = ["推广人", "博主微信", "账号主页链接", "平台", "推广产品，多个产品,隔开", "付费形式", "费用", "佣金",
                  "图文链接", "产出形式", "合作时间"]
        head_row = sheet[1]
        for cell in head_row:
            if cell.value != header[head_row.index(cell)]:
                self.messages.append('表头错误')
                break
        for row in sheet.iter_rows(min_row=2):
            if not row[0].value:
                self.messages.append('第{}行第{}列推广人不能为空'.format(row[0].row, row[0].column))
                return False
        for row in sheet.iter_rows(min_row=2):
            if not row[1].value:
                self.messages.append('第{}行第{}列博主微信不能为空'.format(row[1].row, row[1].column))
                return False
        for row in sheet.iter_rows(min_row=2):
            if not row[2].value:
                self.messages.append('第{}行第{}列账号主页链接不能为空'.format(row[2].row, row[2].column))
                return False
        for row in sheet.iter_rows(min_row=2):
            if not row[3].value:
                self.messages.append('第{}行第{}列平台不能为空'.format(row[3].row, row[3].column))
                return False
        for row in sheet.iter_rows(min_row=2):
            if not row[4].value:
                self.messages.append('第{}行第{}列推广产品，多个产品,隔开不能为空'.format(row[4].row, row[4].column))
                return False
        for row in sheet.iter_rows(min_row=2):
            if not row[5].value:
                self.messages.append('第{}行第{}列付费形式不能为空'.format(row[5].row, row[5].column))
                return False
        for row in sheet.iter_rows(min_row=2):
            if row[6].value == "":
                self.messages.append('第{}行第{}列费用不能为空'.format(row[6].row, row[6].column))
                return False
        for row in sheet.iter_rows(min_row=2):
            if row[7].value == "":
                self.messages.append('第{}行第{}列佣金不能为空'.format(row[7].row, row[7].column))
                return False
        for row in sheet.iter_rows(min_row=2):
            if not row[9].value:
                self.messages.append('第{}行第{}列产出形式不能为空'.format(row[9].row, row[9].column))
                return False

        for row in sheet.iter_rows(min_row=2):
            if not isinstance(row[0].value, str):
                self.messages.append('第{}行第{}列推广人应当是字符串'.format(row[0].row, row[0].column))
                return False
        for row in sheet.iter_rows(min_row=2):
            if not isinstance(row[1].value, str):
                self.messages.append('第{}行第{}列博主微信应当是字符串'.format(row[1].row, row[1].column))
                return False
        for row in sheet.iter_rows(min_row=2):
            if not isinstance(row[2].value, str):
                self.messages.append('第{}行第{}列账号主页链接应当是字符串'.format(row[2].row, row[2].column))
                return False
        for row in sheet.iter_rows(min_row=2):
            if not isinstance(row[3].value, str):
                self.messages.append('第{}行第{}列平台应当是字符串'.format(row[3].row, row[3].column))
                return False
        for row in sheet.iter_rows(min_row=2):
            if not isinstance(row[4].value, str):
                self.messages.append('第{}行第{}列推广产品应当是字符串'.format(row[4].row, row[4].column))
                return False
        for row in sheet.iter_rows(min_row=2):
            if not isinstance(row[5].value, str):
                self.messages.append('第{}行第{}列付费形式应当是字符串'.format(row[5].row, row[5].column))
                return False
        for row in sheet.iter_rows(min_row=2):
            if not isinstance(row[6].value, float) and not isinstance(row[6].value, int):
                print(row[6].value)
                self.messages.append('第{}行第{}列费用应当是浮点类型'.format(row[6].row, row[6].column))
                return False
        for row in sheet.iter_rows(min_row=2):
            if not isinstance(row[7].value, float) and not isinstance(row[7].value, int):
                self.messages.append('第{}行第{}列佣金应当是小数值'.format(row[7].row, row[7].column))
                return False
        for row in sheet.iter_rows(min_row=2):
            if not isinstance(row[8].value, str) and row[8].value != None:
                self.messages.append('第{}行第{}列图文链接应当是字符串'.format(row[8].row, row[8].column))
                return False
        for row in sheet.iter_rows(min_row=2):
            if not isinstance(row[9].value, str):
                self.messages.append('第{}行第{}列产出形式应当是字符串'.format(row[9].row, row[9].column))
                return False
        for row in sheet.iter_rows(min_row=2):
            if not isinstance(row[10].value, datetime) and row[10].value != None:
                self.messages.append('第{}行第{}列产出形式应当是时间序列'.format(row[10].row, row[10].column))
                return False

    def validate(self):
        if self.messages:
            return False
        else:
            return True


if __name__ == '__main__':
    print(HandOrderFile('/Users/zhengyansheng/Desktop/分销商订单模板.xlsx').validate())
