from django.core.management.base import BaseCommand

# from sort_transactions import main
from myFinance import models
from finance.celery_app import load_transactions_by_credential
from django.core.management.base import BaseCommand

from finance.celery_app import load_transactions_by_credential
# from sort_transactions import main
from myFinance import models


class Command(BaseCommand):
    def handle(self, *args, **options):
        load_transactions_by_credential(credential_id= int(options.get('credential_id')), headless=False, grid=False)

    def add_arguments(self, parser):
        parser.add_argument('--credential_id', type=str, help="start date")