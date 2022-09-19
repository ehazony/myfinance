import os
from celery import Celery
from django.core import management
from celery.signals import setup_logging  # noqa

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

