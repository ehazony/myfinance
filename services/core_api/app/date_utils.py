import calendar
import datetime

import dateutil.relativedelta as relativedelta

from myFinance.models import DateInput, Credential


def month_range(date):
    return start_month(date), end_month(date)


def start_month(date):
    """
    first day of the month that contains day
    """
    return date.replace(day=1, minute=0, second=0, microsecond=0)


def end_month(date):
    """
    last day of month that contains date
    """
    if type(date) == datetime.date:
        return date.replace(day=calendar.monthrange(date.year, date.month)[1])
    return date.replace(day=calendar.monthrange(date.year, date.month)[1],
                        minute=0, second=0, microsecond=0)


def next_bill_date(user):
    """
    :returns the next bill date by looking for the last bill date in the credit card Credentials, if it is not found
    defaults to the DateInput start_date
    """
    bill_dates = []
    for c_info in Credential.objects.all().values_list('additional_info', flat=True):
        for detail in c_info.get('card_details', []):
            bill_dates.append(detail['next_bill'])
    bill_day = datetime.datetime.fromisoformat(max(bill_dates)).date() if bill_dates else DateInput.objects.filter(
        user=user, name='start_date').first().date
    now = datetime.datetime.now()
    next_bill = now.replace(day=bill_day.day)
    if bill_day.day < now.day:
        return next_bill + relativedelta.relativedelta(months=1)
    return next_bill


def date_in_bill_month(day, user):
    bill_day = next_bill_date(user)
    try:
        bill_in_month = bill_day.replace(day=day) # day is out of range for month
    except ValueError:
        bill_in_month = bill_day.replace(day=calendar.monthrange(bill_day.year, bill_day.month)[1])

    return bill_in_month if day < bill_day.day else bill_in_month - relativedelta.relativedelta(months=1)
