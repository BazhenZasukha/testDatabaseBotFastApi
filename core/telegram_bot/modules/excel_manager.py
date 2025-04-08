from openpyxl import Workbook



class Manager:
    def __init__(self): pass

    def createWorkbook(self):
        wb = Workbook()
        return wb, wb.active

    def write(self, sheet, col: str, row: int, data: str):
        sheet[f'{col}{row}'] = data


    def save(self, wb: Workbook, filename: str):
        wb.save(filename=filename)