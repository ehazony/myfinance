import datetime

import dateutil
import xlsxwriter
import xlrd
from dateutil import relativedelta

from myFinance.TAG_DB.tag_db_api import tags_file_names

DATE = 0
COMPENY_NAME = 1
PRICE = 2

DB = "C:\\Users\\efrai\\Desktop\\bills\\finance\\bank_statements\\DB"

SAVE_TO_DB = False
DEFULT_DATE = datetime.date.today()


def dump_to_excel_file(sorted_transactions, output_file):
    workbook = xlsxwriter.Workbook(output_file, {'strings_to_numbers': True})
    worksheet = workbook.add_worksheet()

    # Start from the first cell. Rows and columns are zero indexed.
    row = 0
    col = 0

    for i in range(len(tags_file_names)):
        temp_col = +i * 3 + i
        worksheet.write(row, temp_col, tags_file_names[i])
        temp_row = 0
        for element in sorted_transactions[tags_file_names[i]]:
            temp_row += 1
            worksheet.write(temp_row, temp_col, element[DATE])
            worksheet.write(temp_row, temp_col + 1, element[COMPENY_NAME])
            worksheet.write(temp_row, temp_col + 2, element[PRICE])
    workbook.close()


def fix_date(transaction_date, wb):
    flipped = False
    cur_month = DEFULT_DATE.month
    start_month = (DEFULT_DATE - relativedelta.relativedelta(months=1)).replace(day=10)
    end_month = DEFULT_DATE.replace(day=10)

    if type(transaction_date) == float:
        transaction_date = datetime.datetime(*xlrd.xldate_as_tuple(transaction_date, wb.datemode))
        # if not start_month <= date.date() <= end_month:
        #     date month flipped
            # if start_month <= date.replace(month=date.day, day=date.month).date() <= end_month:
            #     date = date.replace(month=date.day, day=date.month)
            #     flipped =True
        # return datetime.datetime.strftime(date, '%d/%m/%y')
    return transaction_date


def load_card_statement(path_name):
    """
    loads transactions from an excel file. (visa cards)
    :returns:  list of tuples  (date, name, value)
    """
    loc = path_name
    temp = list()
    wb = xlrd.open_workbook(loc)
    sheet = wb.sheet_by_index(0)
    sheet.cell_value(0, 0)
    number_rows = sheet.nrows
    print("Transactions in file:")
    print("*"*30)
    for i in range(3, number_rows):
        t = sheet.cell_value(i, 3).split()
        company_name = sheet.cell_value(i, 1)
        transaction_date = fix_date(sheet.cell_value(i, 0), wb)
        # transaction_date = sheet.cell_value(i, 0)
        if len(t) != 0:
            print("payment: " + str(t[1]) + " in date: " + str(transaction_date) + " to company: " + company_name)
            if transaction_date == 'סה"כ:':
                continue
            temp.append((transaction_date, company_name, t[1]))
    print("*"*30)
    return temp



