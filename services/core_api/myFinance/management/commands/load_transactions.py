import datetime

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand

from finance import settings
from finance.celery_app import load_transactions_by_credential
# from sort_transactions import main
from myFinance import models


class Command(BaseCommand):
    start = None
    end = None
    user = None
    credential = None

    def handle(self, *args, **options):
        filter_options = {}
        if options.get("username"):
            filter_options["user__username"] = options.get("username")
        if options.get("credential_id"):
            filter_options["id"] = options.get("credential_id")
        for credential in models.Credential.objects.filter(**filter_options):
            start, end = self.get_date_range(options, credential)
            load_transactions_by_credential(start=start, end=end, credential_id=credential.id)

            # load_transactions_by_credential.apply_async(
            #
            #     **{'start': start.strftime(settings.DEFAULT_TIME_FORMAT) if start else None,
            #        'end': end.strftime(settings.DEFAULT_TIME_FORMAT) if end else None, 'credential_id': credential.id},
            # )

    def add_arguments(self, parser):
        parser.add_argument('--start', type=str, help="start date")
        parser.add_argument('--end', type=str, help="end date")
        parser.add_argument('--username', type=str, help="username")
        parser.add_argument('--credential_id', type=int, help="credential id")

    def get_date_range(self, options, credential):
        start = datetime.datetime.strptime(options.get("start"), '%Y-%m-%d') if options.get("start") else None
        end = datetime.datetime.strptime(options.get("end"), '%Y-%m-%d') if options.get("end") else None

        if not end:
            end = datetime.datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)

        if not start:
            # start = credential.last_scanned + datetime.timedelta(
            #     days=1) if credential.last_scanned else models.DateInput.objects.get(name='last_scanned',
            #                                                                          user=credential.user, ).date
            start = end.replace(day=1)
        return start, end
