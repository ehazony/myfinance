
from bank_scraper import cal, discount,max

def get_transactions(start, end):
    transactions = []
    transactions.extend(cal.get_transactions(start, end))
    print('Done loading Cal')
    transactions.extend(discount.get_discount_transactions(start, end))
    print('Done loading Discount')
    transactions.extend(max.get_transactions(start, end))
    print('Done loading Max')
    return transactions


