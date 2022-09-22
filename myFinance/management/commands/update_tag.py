from django.core.management.base import BaseCommand


#
# from myFinance.TAG_DB.tag_db_api import TagDb
# from myFinance.models import Transaction, Tag
# from sort_transactions import TAG_DB_DIR
#
#
class Command(BaseCommand):
    #
    #     def add_arguments(self, parser):
    #         """
    #         Entry point for subclassed commands to add custom arguments.
    #         """
    #         parser.add_argument('--tag', nargs='+', type=str)
    #
    def handle(self, *args, **options):
        pass

#         tag = Tag.objects.get(name=options['tag'][0])
#         tag_names = TagDb(TAG_DB_DIR).get_tagged_lists()[tag.file_name]
#         for t in tag_names:
#             for transaction in Transaction.objects.filter(name=t):
#                 transaction.tag = tag.name
#                 transaction.save()
