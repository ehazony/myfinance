import datetime
import logging
import os
import traceback

# Set Django settings before any Django imports
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "finance.settings")

# Import Celery before Django to avoid conflicts
from celery import Celery
from celery.signals import setup_logging  # noqa

# DO NOT import Django models or views at module level
# Move all Django imports inside functions to prevent reentrant populate() errors

logger = logging.getLogger(__name__)

# Configure Celery app
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
    # Import Django modules inside the task
    from django.core import management
    management.call_command('load_transactions', **options)


@app.task(bind=True)
def update_user_code(self, **options):
    # Import Django modules inside the task
    from django.core import management
    management.call_command('update_user_code', **options)


# TODO: Move this task to Scraper Service
# This task should be removed from core API and implemented in scraper service
# @app.task(bind=True)
# def load_transactions_by_credential(self, **options):
#     """This task will be moved to scraper service with inter-service communication"""
#     pass


# TODO: Move this task to Telegram Bot Service  
# This task should be removed from core API and implemented in telegram bot service
# @app.task(bind=True)
# def send_telegram_message(self, **options):
#     """This task will be moved to telegram bot service"""
#     pass


@app.task(bind=True)
def send_category_info(self, **options):
    # Import Django modules inside the task to avoid populate() errors
    from django.contrib.auth.models import User
    from app.views import create_continuous_category_summery
    
    user = User.objects.get(username='efraim')
    s = create_continuous_category_summery(user)
    
    # TODO: Replace with service communication to telegram bot service
    # For now, just log the message
    logger.info(f"Category info generated: {s}")
    
    # Future implementation will send to telegram service via HTTP or message queue
    # Example: telegram_service_client.send_message(s)


@app.task(bind=True)
def send_month_day_info(self, **options):
    # Import Django modules inside the task to avoid populate() errors
    from django.contrib.auth.models import User
    from app.views import create_continuous_day_summery
    
    user = User.objects.get(username='efraim')
    s = create_continuous_day_summery(user)
    
    # TODO: Replace with service communication to telegram bot service
    # For now, just log the message
    logger.info(f"Day info generated: {s}")
    
    # Future implementation will send to telegram service via HTTP or message queue
    # Example: telegram_service_client.send_message(s)


# TODO: Add inter-service communication tasks
# @app.task(bind=True)
# def send_to_telegram_service(self, message):
#     """Send message to telegram bot service via HTTP API"""
#     # Implementation will use requests to call telegram service
#     pass

# @app.task(bind=True)  
# def trigger_scraper_task(self, credential_id, start_date, end_date):
#     """Trigger scraper task in scraper service via message queue"""
#     # Implementation will send task to scraper service queue
#     pass
