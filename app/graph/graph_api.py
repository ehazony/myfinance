from django.db.models import Sum

from dateutil import relativedelta
from myFinance.models import *
import plotly.express as px
import pandas as pd


# ----------------------------------------------------------
# Transaction sets types
# ----------------------------------------------------------


def expenses_transactions(user):
	""":returns anything that should not be excluded from the monthly expenses calculation"""
	if not Transaction.objects.filter(user=user):
		return Transaction.objects.filter(user=user)
	start_date = DateInput.objects.get(name='start_date', user=user).date
	end = datetime.datetime.now()
	return Transaction.objects.filter(date__gte=start_date, date__lte=end, user=user).exclude(
		tag__in=['exclude', 'credit cards', 'salary'])


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
	return Transaction.objects.filter(date__gte=start_date, date__lte=end, user=user, tag__in=['salary'])


# ----------------------------------------------------------
# graph functions
# ----------------------------------------------------------

def bar(transaction_set):
	if transaction_set.count() == 0:
		return None
	ts_pd = pd.DataFrame(list(transaction_set))
	fig = px.bar(ts_pd, x='month_date', y='value__sum', color='value__sum')
	return fig


def scatter(transactions_set):
	if transactions_set.count() == 0:
		return None
	transactions_df = pd.DataFrame(list(transactions_set.values()))
	fig = px.scatter(transactions_df, x="date", y="value",
	                 hover_name="tag", hover_data=["name"], color="bank")
	return fig


def line(transactions_set):
	if transactions_set.count() == 0:
		return None
	trans = pd.DataFrame(list(transactions_set))
	fig = px.line(trans, x="month_date", y="value__sum", )
	return fig


# ----------------------------------------------------------
# transactions aggregations
# ----------------------------------------------------------

def bar_fig_by_month(transactions):
	if transactions.count() == 0:
		return None
	aggregated_trans = transactions.values('month_date').annotate(Sum('value'))
	return bar(aggregated_trans)


# ----------------------------------------------------------
# transactions aggregations
# ----------------------------------------------------------

def line_fig_by_month(transactions):
	if transactions.count() == 0:
		return None
	trans = transactions.values('month_date').annotate(Sum('value'))
	return line(trans)


def line_fig_by_tag_by_month(transactions_set):
	trans = transactions_set.values(
		'month_date',
		'tag_ref__name').annotate(
		Sum('value'))
	if trans.count() == 0:
		return None
	trans = pd.DataFrame(list(trans))
	fig = px.line(trans, x="month_date", y="value__sum", color="tag_ref__name", line_group="tag_ref__name",
	              hover_name="tag_ref__name")
	return fig

def line_fig_by_name_by_month(transactions_set):
	trans = transactions_set.values(
		'month_date',
		'name').annotate(
		Sum('value'))
	if trans.count() == 0:
		return None
	trans = pd.DataFrame(list(trans))
	fig = px.line(trans, x="month_date", y="value__sum", color="name", line_group="name",
	              hover_name="name")
	return fig


# ----------------------------------------------------------
# complex figures
# ----------------------------------------------------------


def monthly_average_by_category(user):
	trans = expenses_transactions(user)
	trans = trans.values('tag_ref__name').annotate(Sum('value'))
	if trans.count() == 0:
		return None
	trans = pd.DataFrame(list(trans))

	start_date = DateInput.objects.get(name='start_date', user=user).date
	end = datetime.datetime.now()
	trans["value__sum"] = trans["value__sum"] / number_of_months(user)
	trans = trans.rename(columns={'tag_ref__name': 'tag', 'value__sum': 'monthly average'}, index={'ONE': 'one'})
	trans = trans[['monthly average', 'tag']]
	ts_pd = pd.DataFrame(list(trans))
	fig = px.bar(ts_pd, x=trans['tag'], y=trans['monthly average'], color=trans['monthly average'])
	fig = px.pie(ts_pd, values=trans['monthly average'], names=trans['tag'],
	             color_discrete_sequence=px.colors.sequential.Inferno)
	fig.update_layout(xaxis_title='tag', yaxis_title='monthly average', margin=dict(l=0, r=0, t=0, b=0), )
	return fig

def monthly_average_by_name(transactions, user):
	trans = transactions
	trans = trans.values('name').annotate(Sum('value'))
	if trans.count() == 0:
		return None
	trans = pd.DataFrame(list(trans))

	# start_date = DateInput.objects.get(name='start_date', user=user).date
	# end = datetime.datetime.now()
	trans["value__sum"] = trans["value__sum"] / number_of_months(user)
	trans = trans.rename(columns={'value__sum': 'monthly average'}, index={'ONE': 'one'})
	trans = trans[['monthly average', 'name']]
	ts_pd = pd.DataFrame(list(trans))
	fig = px.bar(ts_pd, x=trans['name'], y=trans['monthly average'], color=trans['monthly average'])
	fig = px.pie(ts_pd, values=trans['monthly average'], names=trans['name'],
	             color_discrete_sequence=px.colors.sequential.Inferno)
	fig.update_layout(xaxis_title='tag', yaxis_title='monthly average', margin=dict(l=0, r=0, t=0, b=0), )
	return fig

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
	return relativedelta.relativedelta(end, start_date).months + 1


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
