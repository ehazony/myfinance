import datetime

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand

from finance.celery_app import load_transactions_by_credential
# from sort_transactions import main
from myFinance import models


class Command(BaseCommand):

    def handle(self, *args, **options):
        start = datetime.datetime.strptime(options.get("start"), '%Y-%m-%d') if options.get("start") else None
        end = datetime.datetime.strptime(options.get("end"), '%Y-%m-%d') if options.get("start") else None
        user = User.objects.get(username='efraim')
        last_scanned = models.DateInput.objects.get(name='last_scanned', user=user, )
        if start and end and end < start:
            raise Exception('start date cannot be after end (was there a scan already done?)')

        for credential in models.Credential.objects.all():
            load_transactions_by_credential.apply_async(
                kwargs={'start': start, 'end': end, 'credential_id': credential.id},
                serializer='pickle',
            )
            # scraper = scraper_factory(credential.company)
            # transactions = scraper.get_transactions(start, end, **credential.get_credential)
            # sorted_transactions = sort_to_categories(transactions)
            # for transaction in sorted_transactions:
            #     bank = transaction.get('bank') if transaction.get('bank') else False
            #     Transaction.objects.create(user=user, arn=transaction.get('arn'),
            #                                date=transaction['date'], name=transaction['name'],
            #                                value=transaction['amount'], tag=transaction['tag'],
            #                                bank=bank)
            # credential.last_scanned = end
            # credential.save()

    def add_arguments(self, parser):
        parser.add_argument('--start', type=str, help="start date")
        parser.add_argument('--end', type=str, help="end date")
