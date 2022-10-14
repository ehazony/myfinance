import datetime
import logging
import os

import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "finance.settings")

django.setup()

from celery import Celery
from celery.signals import setup_logging  # noqa
from django.contrib.auth.models import User
from django.core import management

from app.views import create_continuous_category_summery
from bank_scraper import scraper_factory
from finance import settings
from myFinance import models
from sort_transactions import sort_to_categories
from telegram_bot import telegram_bot_api

logger = logging.getLogger(__name__)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'finance.settings')
app = Celery('app')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()


@setup_logging.connect
def config_loggers(*args, **kwargs):
    from logging.config import dictConfig  # noqa
    from django.conf import settings  # noqa

    dictConfig(settings.LOGGING)


@app.task(bind=True)
def debug_task(self):
    print(f'in debug_task')


@app.task(bind=True)
def load_transactions(self, **options):
    management.call_command('load_transactions', **options)


@app.task(bind=True)
def load_transactions_by_credential(self, **options):
    credential = models.Credential.objects.get(id=options['credential_id'])
    start, end = options.get('start'), options.get('end')
    if not start:
        start = credential.last_scanned + datetime.timedelta(
            days=1) if credential.last_scanned else models.DateInput.objects.get(name='last_scanned',
                                                                                 user=credential.user, ).date
    else:
        start, end = datetime.datetime.strptime(start, settings.DEFAULT_TIME_FORMAT), datetime.datetime.strptime(end,
                                                                                                                 settings.DEFAULT_TIME_FORMAT)
    if not end:
        end = datetime.date.today() - datetime.timedelta(days=1)
    if end < start:
        logger.info('Nothing to do (End < Start)')
        return
    logger.info('starting work for user {} company {}'.format(credential.user, credential.company))
    logger.info('start date: {} , end date: {}'.format(start, end))
    scraper = scraper_factory(credential.company)
    transactions = scraper.get_transactions(start, end, credential, **credential.get_credential)
    sorted_transactions = sort_to_categories(transactions, user=credential.user)
    for transaction in sorted_transactions:
        bank = transaction.get('bank') if transaction.get('bank') else False
        models.Transaction.objects.create(user=credential.user, arn=transaction.get('arn'),
                                          date=transaction['date'], name=transaction['name'],
                                          value=transaction['amount'], tag=transaction['tag'],
                                          bank=bank, credential=credential)
    if end > credential.last_scanned:
        credential.last_scanned = end
        credential.save()
    logger.info('starting work for user {} company {}'.format(credential.user, credential.company))
    logger.info('done work for user {} company {}'.format(credential.user, credential.company))


@app.task(bind=True)
def send_telegram_message(self, **options):
    telegram_bot_api.send_message(options['message'])


@app.task(bind=True)
def send_category_info(self, **options):
    user = User.objects.get(username='efraim')
    s = create_continuous_category_summery(user)
    telegram_bot_api.send_message(s)
