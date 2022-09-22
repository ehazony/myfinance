import calendar
import datetime


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
    return date.replace(day=calendar.monthrange(date.year, date.month)[1],
                        minute=0, second=0, microsecond=0)
