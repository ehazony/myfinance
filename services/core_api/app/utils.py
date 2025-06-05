import datetime

from dateutil import relativedelta
from django.db.models import Sum

from myFinance.models import Transaction, DateInput

def approx_rolling_average(avg, new_sample, n):
    return (avg * (n - 1) + new_sample) / n

def expenses_transactions(user):
    """:returns anything that should not be excluded from the monthly expenses calculation"""
    if not Transaction.objects.filter(user=user).exists():
        return Transaction.objects.filter(user=user)
    start_date = DateInput.objects.get(name='start_date', user=user).date
    end = datetime.datetime.now()
    return Transaction.objects.filter(date__gte=start_date, date__lte=end, user=user).exclude( tag__expense=False,)


def all_transactions_in_dates(user):
    """:returns anything that should not be excluded from the monthly expenses calculation"""
    if not Transaction.objects.filter(user=user):
        return Transaction.objects.filter(user=user)
    start_date = DateInput.objects.get(name='start_date', user=user).date
    end = datetime.datetime.now()
    return Transaction.objects.filter(date__gte=start_date, date__lte=end, user=user)


def income_transactions(user):
    """:returns anything that should not be excluded from the monthly expenses calculation"""
    if not Transaction.objects.filter(user=user).exists():
        return Transaction.objects.filter(user=user)
    start_date = DateInput.objects.get(name='start_date', user=user).date
    end = Transaction.objects.order_by('month_date').last().month_date
    return Transaction.objects.filter(date__gte=start_date, user=user, tag__name__in=['Salary'])


def average_expenses(user):
    trans = expenses_transactions(user)
    if not trans.exists():
        return 0
    some = trans.aggregate(Sum('value'))['value__sum']
    return round(some / number_of_months(user))


def average_bank_expenses(user):
    trans = expenses_transactions(user)
    trans = trans.filter(bank=True)
    if not trans.exists():
        return 0
    some = trans.aggregate(Sum('value'))['value__sum']
    return round(some / number_of_months(user))


def average_income(user):
    trans = income_transactions(user)
    if not trans.exists():
        return 0
    some = trans.aggregate(Sum('value'))['value__sum']
    end = Transaction.objects.filter(user=user).order_by('month_date').last().month_date
    if end > datetime.date.today():
        end = datetime.date.today()
    return -round(some / number_of_months(user))


def number_of_months(user):
    if not Transaction.objects.filter(user=user).exists():
        return 0
    start_date = DateInput.objects.get(name='start_date', user=user).date
    end = Transaction.objects.filter(user=user).order_by('month_date').last().month_date
    if end > datetime.date.today():
        end = datetime.date.today()
    delta = relativedelta.relativedelta(end, start_date)
    return delta.years * 12 + delta.months + 1
