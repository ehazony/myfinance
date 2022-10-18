import datetime
import random

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand

from myFinance import models


class Command(BaseCommand):

    def handle(self, *args, **options):
        for user in User.objects.all():
            ad, created = models.AdditionalInfo.objects.get_or_create(user= user)
            ad.value['user_code'] = models.AdditionalInfo.create_user_code()
            ad.save()