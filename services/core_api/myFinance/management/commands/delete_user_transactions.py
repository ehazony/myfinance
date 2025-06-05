import datetime

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand

from finance.celery_app import load_transactions_by_credential
# from sort_transactions import main
from myFinance import models


class Command(BaseCommand):

    def handle(self, *args, **options):
        # start = datetime.datetime.strptime(options.get("start"), '%Y-%m-%d') if options.get("start") else None
        # end = datetime.datetime.strptime(options.get("end"), '%Y-%m-%d') if options.get("start") else None
        user = User.objects.get(username=options.get('username'))
        now = datetime.datetime.now()
        models.Transaction.objects.filter(user=user, date__year=now.year, date__month=now.month).delete()
        for credential in models.Credential.objects.filter(user= user):
            before_start_month = now.replace(day=1, minute=0,second=0,microsecond=0) - datetime.timedelta(days=1)
            if credential.last_scanned and before_start_month.date() < credential.last_scanned:
                credential.last_scanned = before_start_month
                credential.save()

    def add_arguments(self, parser):
        # parser.add_argument('--start', type=str, help="start date")
        # parser.add_argument('--end', type=str, help="end date")
        parser.add_argument('--username', type=str, help="username")