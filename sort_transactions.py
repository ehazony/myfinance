from myFinance.models import TransactionNameTag, Tag


def sort_to_categories(transaction_statements, user):
    """
    """
    print("started sorting to categories:")
    print("*" * 30)
    for transaction in transaction_statements:
        tag = TransactionNameTag.get_tag(transaction['name'], user)
        if not tag:
            tag = Tag.objects.get(user=user, key='other')

        transaction['tag'] = tag
    print("*" * 30)
    return transaction_statements


def get_category(transaction_statement):
    tag = TransactionNameTag.get_tag(transaction_statement['name'], transaction_statement['user'])
    if not tag:
        tag = Tag.objects.get(user=transaction_statement['user'], key='other')
    return tag
