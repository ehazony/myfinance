from abc import abstractmethod

from myFinance.models import TransactionNameTag


class ExcelParser:
    @abstractmethod
    def load_transactions(self, ws, user):
        pass

    @abstractmethod
    def is_right_format(self, ws):
        pass


class CalExcelParser(ExcelParser):

    def load_transactions(self, ws, user):
        pass

    def is_right_format(self, ws):
        lines = list(ws.iter_rows())
        A1 = "פירוט עסקות נכון לתאריך"
        if


def load_excel_file(ws, user):
    sorted_transactions = list()
    unsorted_transactions = list()
    # iterating over the rows and
    # getting value from each cell in row
    for row in list(ws.iter_rows()):
        if not row[1].value or not row[3].value or not row[0].value:
            continue
        row_data = {}
        row_data["name"] = row[1].value
        row_data["value"] = row[3].value.replace("₪", "").replace(",", "").strip()
        row_data["date"] = row[0].value
        tag = TransactionNameTag.get_tag(row_data["name"], user)
        if tag:
            row_data["tag"] = tag.name
            sorted_transactions.append(row_data)
        else:
            unsorted_transactions.append(row_data)
    return sorted_transactions + unsorted_transactions
