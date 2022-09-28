import datetime
import json

from django.conf import settings
from django.contrib.postgres.fields import JSONField
from django.db import models
from django_kms.fields import KMSEncryptedCharField


class DateInput(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=128)
    date = models.DateField()


class Tag(models.Model):
    OTHER = 'other'
    SALARY = 'salary'
    key = models.CharField(max_length=128, null=True)
    name = models.CharField(max_length=128)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)
    expense = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name


class TagGoal(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE, null=True)
    value = models.FloatField()


class Transaction(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)
    date = models.DateField()
    name = models.CharField(max_length=200)
    value = models.FloatField()
    month = models.IntegerField(null=True)
    tag = models.ForeignKey(Tag, null=True, on_delete=models.SET_NULL)
    month_date = models.DateField(null=True)
    bank = models.BooleanField(default=False)
    arn = models.CharField(max_length=64, null=True)
    __original_tag = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__original_tag = self.tag

    def get_month(self):
        start_date = DateInput.objects.get(name="start_date", user=self.user).date
        if self.date.day >= start_date.day:
            return self.date.month
        else:
            return 12 if self.date.month == 1 else self.date.month - 1

    def get_month_date(self):
        start_date = DateInput.objects.get(name="start_date", user=self.user).date
        if self.date.day < start_date.day:
            return (self.date - datetime.timedelta(days=start_date.day)).replace(day=start_date.day)
        else:
            return self.date.replace(day=start_date.day)

    def save(self, *args, **kwargs):
        self.month = self.get_month()
        self.month_date = self.get_month_date()
        if self._state.adding or self.tag != self.__original_tag:  # only when new instance or tag changed
            TransactionNameTag.objects.update_or_create(user=self.user, transaction_name=self.name,
                                                        defaults={'tag': self.tag})
        super(Transaction, self).save(*args, **kwargs)
        self.__original_tag = self.tag


class TransactionNameTag(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)
    transaction_name = models.CharField(max_length=200)
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'transaction_name')

    @classmethod
    def get_tag(cls, name, user):
        trnt = TransactionNameTag.objects.filter(transaction_name=name, user=user).first()
        return trnt.tag if trnt else None


class Plan(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)
    date = models.DateField()
    value = models.FloatField()


class AdditionalInfo(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    value = JSONField()


class DiscountCredential(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)
    password = KMSEncryptedCharField(key_id="7388ca30-4279-45cc-a05e-f05f9fb7d4af")
    user_identification = KMSEncryptedCharField(key_id="7388ca30-4279-45cc-a05e-f05f9fb7d4af")
    user_name = KMSEncryptedCharField(key_id="7388ca30-4279-45cc-a05e-f05f9fb7d4af")


class Credential(models.Model):
    DISCOUNT = 'DISCOUNT'
    CAL = 'CAL'
    MAX = 'MAX'

    BANK = 'BANK'
    CARD = 'DEBIT_CARD'

    ADDITIONAL_INFO_BALANCE = 'balance'
    COMPANY_CHOICES = (
        (DISCOUNT, "Discount"),
        (CAL, "Cal"),
        (MAX, "Max"),
    )
    TYPE_CHOICES = ((BANK, 'Bank'), (CARD, 'Debit Card'),)

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)
    company = models.CharField(max_length=30, choices=COMPANY_CHOICES, default="1")
    credential = KMSEncryptedCharField(key_id="7388ca30-4279-45cc-a05e-f05f9fb7d4af")
    last_scanned = models.DateField(null=True)
    type = models.CharField(max_length=32, choices=TYPE_CHOICES, default="1")
    additional_info = JSONField(default={})

    def save(self, *args, **kwargs):
        if type(self.credential) == dict:
            self.credential = json.dumps(self.credential)
        super(Credential, self).save(*args, **kwargs)

    @property
    def get_credential(self):
        return json.loads(self.credential)

    @property
    def balance(self):
        return self.additional_info.get('balance')


