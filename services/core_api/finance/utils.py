import datetime
from functools import reduce

from myFinance import serialisers
from myFinance.models import Transaction
from sort_transactions import get_category


def is_transaction(transaction_fields, transaction):
    return reduce((lambda x, y: x and y),
                  map(lambda key: getattr(transaction, key) == transaction_fields[key] if hasattr(transaction,
                                                                                                  key) else True,
                      [key for key in transaction_fields.keys() if
                       key != 'tag']))  # TODO change when change to category


def update_transactions(credential, transaction_list):
    transaction_list_sorted = sorted(transaction_list, key=lambda x: (x['date'], x['name'], x['value']))
    if not transaction_list_sorted:
        return
    first_date, end_date = transaction_list_sorted[0]['date'], transaction_list_sorted[-1]['date']
    db_transactions = credential.transaction_set.filter(date__gte=first_date, date__lte=end_date).order_by('date',
                                                                                                           'name',
                                                                                                           'value')

    db_transactions_list = list(db_transactions)
    i = 0
    identifier = bool(transaction_list_sorted[0].get('identifier'))
    for current in transaction_list_sorted:
        if type(current['date']) == datetime.datetime:
            current['date'] = current['date'].date()
        if identifier:
            if db_transactions.filter(identifier=current['identifier'], credential=credential).exists():
                continue
        else:
            if i < len(db_transactions_list) and is_transaction(current, db_transactions_list[i]):
                i += 1
                continue
        current['credential'] = credential.id
        current['user'] = credential.user.id
        current['tag'] = get_category(current).id
        serializer = serialisers.TransactionSerializer(data=current)
        if serializer.is_valid():
            serializer.save()
        else:
            raise Exception('could not validate transaction for credential: ' + credential.company)


def remove_duplicate_transactions(transaction_list):
    for t in transaction_list.values('user', 'date', 'name', 'value').distinct():
        Transaction.objects.filter(
            pk__in=Transaction.objects.filter(**t).values_list('id', flat=True)[1:]).delete()
