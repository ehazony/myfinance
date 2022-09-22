import datetime

import django

from myFinance.models import TransactionNameTag, Tag

django.setup()
from myFinance.TAG_DB.tag_db_api import TagDb, tags_names, all_tags

from sorting.xl_api import load_card_statement, dump_to_excel_file
import os
# from sorting.save_to_db import save_transaction
from finance.settings import BASE_DIR

DATE = 'date'
COMPENY_NAME = 'name'
PRICE = 'amount'

DB_DIR = BASE_DIR + "\\bank_statements\\DB\\"
INPUT_FILE_DIR = BASE_DIR + "\\bank_statements\\temp"
TAG_DB_DIR = BASE_DIR + "\\bank_statements\\DB"
SAVE_TO_DB = False
DEFULT_DATE = datetime.date.today()


def print_tag_indexes():
    i = 0
    for tag in all_tags:
        print(str(i) + " - " + tag.name)
        i += 1


def get_tag_from_user(transaction):
    while (True):
        print("****************")
        print_tag_indexes()
        print("transaction not in DB")
        print("payment: " + str(transaction[PRICE]) + " in date: " + str(transaction[DATE]) + " to company: " +
              transaction[COMPENY_NAME])
        tag_number = int(input("inter number " + str(0) + "-" + str(len(tags_names) - 1) + ":"))
        print("****************")
        if int(tag_number) < len(tags_names):
            return all_tags[tag_number]
        else:
            print("not a valid input, try again...")


def save_transactions(sorted_transactions):
    for tag_file_name, transactions_list in sorted_transactions.items():
        tag_name = tag_file_name.replace(".txt", "")
        for item in transactions_list:
            date, name, price = item[0], item[1], float(item[2].replace(',', ''))
            save_transaction(date, name, price, tag_name)


def main(input_dir=INPUT_FILE_DIR, output_dir="", tag_db_dir=TAG_DB_DIR):
    # global DEFULT_DATE
    tag_db = TagDb(tag_db_dir)

    i = 1
    SAVE_TO_DB = input("save results to db?") == 'yes'
    # if SAVE_TO_DB:
    #     DEFULT_DATE = DEFULT_DATE.replace(month=int(input("witch month should be set as default?")))
    for file in os.listdir(input_dir):
        if file.endswith(".xlsx") and file[0] != '~':
            print("file: {}".format(file))
            taged_lists = tag_db.get_tagged_lists()
            transaction_statements = load_card_statement(input_dir + "\\" + file)
            sorted_transactions = sort_to_categories(transaction_statements, tag_db)  # TODO Deprecated
            dump_to_excel_file(sorted_transactions, output_dir + "{}_out_{}.xlsx".format(file, i))
            if SAVE_TO_DB:
                save_transactions(sorted_transactions)
            i += 1


def sort_to_categories(transaction_statements, user, default_other=True):  # remade to work with DB
    """
    """
    print("started sorting to categories:")
    print("*" * 30)
    print_tag_indexes()
    for transaction in transaction_statements:
        tag = TransactionNameTag.get_tag(transaction['name'], user)
        if not tag:
            if default_other:
                tag = Tag.objects.get(user=user, name='Other')
            else:
                tag = get_tag_from_user(transaction)  # TODO add user
                TransactionNameTag.objects.create(user=user, transaction_name=transaction['name'], tag=tag)

        transaction['tag'] = tag
    print("*" * 30)
    return transaction_statements


if __name__ == "__main__":
    main()
