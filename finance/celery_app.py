import datetime
import logging
import os

import django
import traceback

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "finance.settings")

django.setup()

from celery import Celery
from celery.signals import setup_logging  # noqa
from django.contrib.auth.models import User
from django.core import management

from app.views import create_continuous_category_summery, create_continuous_day_summery
from bank_scraper.base import scraper_factory
from finance import settings, utils
from myFinance import models
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
def update_user_code(self, **options):
    management.call_command('update_user_code', **options)


@app.task(bind=True)
def load_transactions_by_credential(self, **options):
    credential = models.Credential.objects.get(id=options.get('credential_id'))
    start, end = options.get('start'), options.get('end')
    if end < start:
        logger.info('Nothing to do (End < Start)')
        return
    logger.info('starting work for user {} company {}'.format(credential.user, credential.company))
    logger.info('start date: {} , end date: {}'.format(start, end))
    try:
        scraper = scraper_factory(credential.company)
        transactions = scraper.get_transactions(start, end, credential, **credential.get_credential,
                                                headless=options.get('headless', False),
                                                grid=options.get('grid', False))
        utils.update_transactions(credential, transactions, )
        if not credential.last_scanned or end.date() > credential.last_scanned:
            credential.last_scanned = end.date()
            credential.save()
    except Exception as e:
        raise e
        trace = traceback.format_exc()
        message = 'Error loading Transactions for company {}: {}'.format(credential.company, trace)
        models.ErrorLog.objects.create(user=credential.user, message={'error': message})
        logger.error(message)
        telegram_bot_api.send_message(message)

    logger.info('done work for user {} company {}'.format(credential.user, credential.company))


@app.task(bind=True)
def send_telegram_message(self, **options):
    telegram_bot_api.send_message(options['message'])


@app.task(bind=True)
def send_category_info(self, **options):
    user = User.objects.get(username='efraim')
    s = create_continuous_category_summery(user)
    telegram_bot_api.send_message(s)


@app.task(bind=True)
def send_month_day_info(self, **options):
    user = User.objects.get(username='efraim')
    s = create_continuous_day_summery(user)
    telegram_bot_api.send_message(s)
