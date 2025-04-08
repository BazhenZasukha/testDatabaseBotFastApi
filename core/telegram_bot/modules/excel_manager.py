from openpyxl import Workbook



class Manager:
    def __init__(self): pass

    def createWorkbook(self):
        wb = Workbook()
        sheet = wb.active

        self.write(sheet, 'A', 1, 'ID')
        self.write(sheet, 'B', 1, 'DATE')
        self.write(sheet, 'C', 1, 'PRICE (UAH)')
        self.write(sheet, 'D', 1, 'PRICE (USD)')
        self.write(sheet, 'E', 1, '1 USD PRICE')
        self.write(sheet, 'F', 1, 'DESCRIPTION')

        # NEW DATA WILL BE ON 2nd LINE

        return wb, sheet

    def write(self, sheet, col: str, row: int, data: str):
        sheet[f'{col}{row}'] = data


    def save(self, wb: Workbook, filename: str):
        wb.save(filename=filename)