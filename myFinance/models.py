from django.conf import settings
from django.db import models
import datetime


class DateInput(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=128)
    date = models.DateField()


class Tag(models.Model):
    name = models.CharField(max_length=128)
    file_name = models.CharField(max_length=128, null=True, blank=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)
    expense = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.file_name:
            self.file_name = self.name + '.txt'
        super(Tag, self).save(*args, **kwargs)


class Transaction(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)
    date = models.DateField()
    name = models.CharField(max_length=200)
    value = models.FloatField()
    tag = models.CharField(max_length=50)
    month = models.IntegerField(null=True)
    tag_ref = models.ForeignKey(Tag, null=True, on_delete=models.SET_NULL)
    month_date = models.DateField(null=True)
    bank = models.BooleanField(default=False)

    def get_month(self):
        start_date = DateInput.objects.get(name="start_date", user= self.user).date
        if self.date.day >= start_date.day:
            return self.date.month
        else:
            return 12 if self.date.month == 1 else self.date.month - 1

    def get_month_date(self):
        start_date = DateInput.objects.get(name="start_date", user = self.user).date
        if self.date.day < start_date.day:
            return (self.date - datetime.timedelta(days=start_date.day)).replace(day=start_date.day)
        else:
            return self.date.replace(day=start_date.day)

    def save(self, *args, **kwargs):
        self.month = self.get_month()
        self.month_date = self.get_month_date()

        try:
            self.tag_ref = Tag.objects.get(user=self.user, name=self.tag)

        except:
            raise Exception("tag matching tag name '{}' dose not exist".format(self.tag))
        super(Transaction, self).save(*args, **kwargs)


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

class  Plan(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)
    date = models.DateField()
    value = models.FloatField()
