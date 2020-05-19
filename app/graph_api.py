from django.db.models import Sum

from myFinance.models import *
import plotly.express as px
import pandas as pd


def bar_fig_by_month(transactions):
    if transactions.count() == 0:
        return None
    ts_pd = pd.DataFrame(list(transactions))
    fig = px.bar(ts_pd, x='month_date', y='value__sum', color='value__sum')
    return fig


def monthly_by_name(user, _name):
    transaction_sum = Transaction.objects.all().filter(name=_name, user=user).values('month_date').annotate(
        Sum('value'))
    return bar_fig_by_month(transaction_sum)


def bar_monthly_by_tag(user, _tag):
    transaction_sum = Transaction.objects.all().filter(tag_ref=_tag, user=user).values('month_date').annotate(
        Sum('value'))
    return bar_fig_by_month(transaction_sum)


def to_df(transactions_set):
    return pd.DataFrame(list(transactions_set.values()))


def transactions_df(user):
    transactions = Transaction.objects.filter(user=user).order_by('date')
    transactions_df = pd.DataFrame(list(transactions.values()))
    return transactions_df


def transactions_sett(user):
    transactions = Transaction.objects.filter(user=user).order_by('date')
    return transactions


def scatter(transactions_set):
    transactions_df = to_df(transactions_set)
    fig = px.scatter(transactions_df, x="date", y="value",
                     hover_name="tag", hover_data=["name"])
    return fig


# ----------------------------------------------------------

def monthly_average_by_category(user):
    trans = Transaction.objects.filter(month__in=[12, 1, 2, 3], user=user).values('tag_ref__name').annotate(
        Sum('value'))
    if trans.count() == 0:
        return None
    trans = pd.DataFrame(list(trans))
    trans["value__sum"] = trans["value__sum"] / 4
    trans = trans.rename(columns={'tag_ref__name': 'tag', 'value__sum': 'monthly average'}, index={'ONE': 'one'})
    trans = trans[['monthly average', 'tag']]
    ts_pd = pd.DataFrame(list(trans))
    fig = px.bar(ts_pd, x=trans['tag'], y=trans['monthly average'], color=trans['monthly average'])
    fig.update_layout(xaxis_title='tag', yaxis_title='monthly average', margin=dict(l=0, r=0, t=0, b=0), )
    return fig


def total_by_month_bar(user):
    transaction_sum = Transaction.objects.filter(user=user).values('month_date').annotate(Sum('value'))
    if transaction_sum.count() == 0:
        return None
    return bar_fig_by_month(transaction_sum)


def total_by_month_line(user):
    trans = Transaction.objects.filter(month__in=[12, 1, 2, 3, 4], user=user).values('month_date').annotate(Sum('value'))
    if trans.count() == 0:
        return None
    trans = pd.DataFrame(list(trans))
    fig = px.line(trans, x="month_date", y="value__sum", )
    return fig


def all_by_tag(user):
    trans = Transaction.objects.filter(month__in=[12, 1, 2, 3, 4], user=user).values('month_date',
                                                                                     'tag_ref__name').annotate(
        Sum('value'))
    if trans.count() == 0:
        return None
    trans = pd.DataFrame(list(trans))

    fig = px.line(trans, x="month_date", y="value__sum", color="tag_ref__name", line_group="tag_ref__name",
                  hover_name="tag_ref__name")
    return fig


def accumelatating_by_month(user):
    # only works for one month.
    trans = Transaction.objects.filter(month__in=[12], user=user).order_by('date').values('name', 'month', 'date',
                                                                                          'value')
    if trans.count() == 0:
        return None
    df = pd.DataFrame(list(trans))
    df['date'] = df['date'].astype('datetime64[ns]')
    gb = df.set_index('date').groupby([pd.Grouper(freq='D'), 'month']).sum().cumsum()
    fig = px.line(gb, x=df.date.unique(), y="value")

    trans = Transaction.objects.filter(month__in=[1], user=user).order_by('date').values('month', 'date', 'value')
    if trans.count() == 0:
        return None
    df = pd.DataFrame(list(trans))
    gb = df.groupby(["month", "date"]).sum().cumsum()
    fig1 = px.line(gb, x=df.date.unique(), y="value")
    fig.add_trace(fig1.data[0])

    trans = Transaction.objects.filter(month__in=[2], user=user).order_by('date').values('month', 'date', 'value')
    if trans.count() == 0:
        return None
    df = pd.DataFrame(list(trans))
    gb = df.groupby(["month", "date"]).sum().cumsum()
    fig1 = px.line(gb, x=df.date.unique(), y="value")
    fig.add_trace(fig1.data[0])

    trans = Transaction.objects.filter(month__in=[3], user=user).order_by('date').values('month', 'date', 'value')
    if trans.count() == 0:
        return None
    df = pd.DataFrame(list(trans))
    gb = df.groupby(["month", "date"]).sum().cumsum()
    fig1 = px.line(gb, x=df.date.unique(), y="value")
    fig.add_trace(fig1.data[0])

    trans = Transaction.objects.filter(month__in=[4], user=user).order_by('date').values('month', 'date', 'value')
    if trans.count() == 0:
        return None
    df = pd.DataFrame(list(trans))
    gb = df.groupby(["month", "date"]).sum().cumsum()
    fig1 = px.line(gb, x=df.date.unique(), y="value")
    fig.add_trace(fig1.data[0])
    return fig


def scatter_by_tag(user, tag):
    transactions = transactions_sett(user).filter(tag_ref=tag)
    if transactions.count() == 0:
        return None
    return scatter(transactions)


def line_by_tag(user, tag):
    trans = Transaction.objects.all().filter(tag_ref=tag).values('month_date').annotate(Sum('value'))
    if trans.count() == 0:
        return None
    trans = pd.DataFrame(list(trans))
    fig = px.line(trans, x="month_date", y="value__sum", )
    return fig
