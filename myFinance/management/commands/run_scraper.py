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
        c = models.Credential.objects.first()
        load_transactions_by_credential(credential_id= 2, headless=False, grid=False)
