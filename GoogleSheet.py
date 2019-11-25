import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import date
from gspread_formatting import *
import time

class GoogleSheet():
    def __init__(self, sheet_name, worksheet_name, worksheet_total_rows, worksheet_total_columns):
        self.sheet_name = sheet_name
        self.worksheet_name = worksheet_name
        self.worksheet_total_rows = worksheet_total_rows
        self.worksheet_total_columns = worksheet_total_columns
        self.scope = ["https://spreadsheets.google.com/feeds",'https://www.googleapis.com/auth/spreadsheets',"https://www.googleapis.com/auth/drive.file","https://www.googleapis.com/auth/drive"]
        self.creds = ServiceAccountCredentials.from_json_keyfile_name("secret.json", self.scope)
        self.client = gspread.authorize(self.creds)
        self.sheet = self.client.open(self.sheet_name)
        self.worksheet = self.sheet.add_worksheet(title=worksheet_name, rows=self.worksheet_total_rows, cols=self.worksheet_total_columns)
        self.sheet_id = self.worksheet._properties['sheetId']

        self.resize('COLUMNS', 0, 1, 450)
        self.resize('COLUMNS', 1, 2, 350)
        self.resize('COLUMNS', 2, 8, 180)
        self.resize('ROWS', 0, 1, 150)
        self.resize('ROWS', 1, self.worksheet_total_rows, 250)

        self.create_default_columns_names()
        self.apply_formatting()


    # object to resize: 'COLUMNS' or 'ROWS', start_index 0-1 means column A or first row
    def resize(self, object_to_resize, start_index, end_index, pixel_size):
        body = {
            "requests": [
                {
                    "updateDimensionProperties": {
                        "range": {
                            "sheetId": self.sheet_id,
                            "dimension": object_to_resize,
                            "startIndex": start_index,
                            "endIndex": end_index
                        },
                        "properties": {
                            "pixelSize": pixel_size
                        },
                        "fields": "pixelSize"
                    }
                }
            ]
        }
        res = self.sheet.batch_update(body)

    def create_default_columns_names(self):
        today = date.today()
        timestamp = today.strftime("%d/%m/%Y")
        self.worksheet.update_cell(1, 1, 'LINK DO AUKCJI')
        self.worksheet.update_cell(1, 2, 'ZDJĘCIE PODGLĄDOWE')
        self.worksheet.update_cell(1, 3, 'CENA')
        self.worksheet.update_cell(1, 4, 'WYSYŁKA')
        self.worksheet.update_cell(1, 5, 'ILOŚĆ SPRZEDANYCH NA DZIEŃ {}'.format(timestamp))
        self.worksheet.update_cell(1, 6, 'NAZWA KATEGORII')
        self.worksheet.update_cell(1, 7, 'ID KATEGORII')
        self.worksheet.update_cell(1, 8, 'SKU')
        self.worksheet.update_cell(1, 9, 'AUKCJA PROMOWANA')

    def update_rows_in_batch(self, row_value_list, first_row, first_column, last_row, last_column):
        cell_list = self.worksheet.range(first_row, first_column, last_row, last_column)
        for cell, value in zip(cell_list, row_value_list):
            cell.value = value
        self.worksheet.update_cells(cell_list, value_input_option='USER_ENTERED')

    def apply_formatting(self):
        fmt_columns = cellFormat(
            backgroundColor=color(0, 128, 128),
            textFormat=textFormat(bold=True, foregroundColor=color(255, 255, 255), fontSize=14),
            horizontalAlignment='CENTER',
            verticalAlignment='MIDDLE',
            wrapStrategy='WRAP'
        )

        fmt_rows = cellFormat(
            textFormat=textFormat(bold=True, foregroundColor=color(255, 255, 255), fontSize=14),
            horizontalAlignment='CENTER',
            verticalAlignment='MIDDLE',
            wrapStrategy='WRAP'
        )
        format_cell_range(self.worksheet, 'A1:I1', fmt_columns)
        format_cell_range(self.worksheet, 'A2:I300', fmt_rows)
        set_frozen(self.worksheet, rows=1, cols=0)
