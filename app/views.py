# -*- encoding: utf-8 -*-
"""
License: MIT
Copyright (c) 2019 - present AppSeed.us
"""
import calendar
import datetime

from bootstrap_modal_forms.generic import BSModalFormView
from dateutil.relativedelta import relativedelta
from django.db.models import Sum, Max, Min
from django.forms import formset_factory
from django.shortcuts import render
from django.urls import reverse_lazy
from rest_framework import status
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.views import APIView

import app.utils
from app.forms import TransactionForm
from myFinance import models
from myFinance.models import Transaction, TransactionNameTag, DateInput, Tag, Credential, RecurringTransaction
from myFinance.serialisers import (
    TransactionRestSerializer,
    TagSerializer,
    CredentialSerializer,
    TagGoalSerializer,
    UserSerializer,
    RecurringTransactionSerializer,
    SummeryWidgetsSerializer,
    MonthTrackingSerializer,
    MonthCategorySerializer,
    BankInfoSerializer,
    TotalMonthExpensesSerializer,
    UserTransactionsNamesSerializer,
    CredentialTypesSerializer,
)
from telegram_bot import telegram_bot_api
from .date_utils import date_in_bill_month, next_bill_date, end_month
from .forms import TransactionModelForm
from .utils import expenses_transactions, average_income
from .models import Conversation, Message
from .serializers import MessageSerializer

# from app.graph.graph_api import monthly_average_by_category, line_fig_by_tag_by_month, line_fig_by_month, \
#     Tag, \
#     bar_fig_by_month, expenses_transactions, scatter, all_transactions_in_dates, average_expenses, average_income, \
#     number_of_months, average_bank_expenses, monthly_average_by_name

NO_DATA_HTML = "<div id=chartContainer style=height: 360px; width: 100%;> No data found</div>"


#######################################################################
#  Views
#######################################################################


class SummeryWidgetsView(APIView):
    serializer_class = SummeryWidgetsSerializer

    def get(self, request, format=None):
        data = {}
        start_date = DateInput.objects.filter(user=request.user, name='start_date')
        if start_date.exists():
            transactions_exp = app.utils.expenses_transactions(request.user)
            # transactions_all = graph_api.all_transactions_in_dates(request.user)
            if transactions_exp.count() == 0:
                return None
            aggregated_trans = transactions_exp.values('month_date').annotate(Sum('value'))
            data = aggregated_trans
            # data = load_index_figures(request.user)

        return Response({"graphs": {"total_expenses_by_month_bar": {'dates': [d['month_date'] for d in data],
                                                                    'series': [d['value__sum'] for d in data]}},
                         "average_expenses": app.utils.average_expenses(request.user),
                         "average_income": average_income(request.user),
                         "number_of_months": app.utils.number_of_months(request.user),
                         "average_bank_expenses": app.utils.average_bank_expenses(request.user)})


class TransactionCreateView(BSModalFormView):
    template_name = 'forms/create_transaction.html'
    form_class = TransactionModelForm

    def form_valid(self, form):
        if 'date' in self.request.POST:
            print('got date {}'.format(self.request.POST.get('date')))

        response = super().form_valid(form)
        return response

    def get_success_url(self):
        day = self.request.POST.get('date')
        date = datetime.date.today().replace(day=int(day))
        DateInput.objects.get_or_create(user=self.request.user, name='start_date', defaults={'date': date})
        return reverse_lazy('home')


class MonthTrackingView(APIView):
    serializer_class = MonthTrackingSerializer

    def get(self, request, format=None):
        s = create_continuous_category_summery(request.user)
        telegram_bot_api.send_message(s)
        return Response(data={'text': s})


class MonthCategoryView(APIView):
    serializer_class = MonthCategorySerializer

    def get(self, request, format=None):
        Pas = [
            "rgb(102, 197, 204)",
            "rgb(246, 207, 113)",
            "rgb(248, 156, 116)",
            # "rgb(220, 176, 242)",
            "rgb(135, 197, 95)",
            "rgb(158, 185, 243)",
            # "rgb(254, 136, 177)",
            # "rgb(201, 219, 116)",
            "rgb(139, 224, 164)",
            # "rgb(180, 151, 231)",
            "rgb(179, 179, 179)",
        ]
        data = []
        if 'month' in request.GET:
            start_month = datetime.datetime.strptime(request.GET['month'], '%Y%m')
        else:
            start_month = datetime.datetime.now().replace(day=1, minute=0, second=0, microsecond=0)
        end_month = start_month.replace(day=calendar.monthrange(start_month.year, start_month.month)[1],
                                        minute=0, second=0, microsecond=0)
        transactions = Transaction.objects.exclude(tag__expense=False, tag__key__in=['credit_cards', 'exclude']).filter(
            date__gte=start_month,
            date__lte=end_month,
            user=request.user)
        if 'category' in request.GET:
            transactions = transactions.filter(tag__name__in=request.GET['category'])

        tag_sums = transactions.values('tag_id').annotate(Sum('value'))
        for i, tag_sum in enumerate(tag_sums):
            tag = Tag.objects.get(id=tag_sum['tag_id'])
            # diff = int(tag.taggoal_set.first().value) - tag_sum['value__sum']
            # value_sum = round(tag_sum['value__sum']) if diff >= 0 else '*{}*'.format(round(tag_sum['value__sum']))
            value = round(tag_sum['value__sum'])
            goal = int(tag.taggoal_set.first().value) if tag.taggoal_set.first() else 0

            data.append(
                {'category_id': tag.id, 'category': tag.name, 'key': tag.name, 'value': value, 'goal': goal,
                 'type': tag.type,
                 'percent': value / goal * 100 if goal and goal > 0 else 100,
                 'color': Pas[i % len(Pas)]})
        return Response(data)


class BankInfo(APIView):
    serializer_class = BankInfoSerializer
    def get(self, request, format=None):
        start_month = datetime.datetime.now().replace(day=1, minute=0, second=0, microsecond=0)
        end_month = datetime.datetime.now().replace(day=calendar.monthrange(start_month.year, start_month.month)[1],
                                                    minute=0, second=0, microsecond=0)
        now = datetime.datetime.now()
        avg_monthly_income = app.utils.average_income(request.user)
        avg_monthly_expenses = app.utils.average_expenses(request.user)
        bank_credentials = models.Credential.objects.filter(user=request.user)
        bank_balance = total_balance = 0
        for cred in bank_credentials:
            bank_balance += cred.balance if cred.balance and cred.type == models.Credential.BANK else 0
            total_balance += cred.balance if cred.balance else 0
        bank_balance = round(bank_balance, 2)
        total_balance = round(total_balance, 2)
        estimated_recurring_transactions_month = RecurringTransaction.objects.filter(user=request.user,
                                                                                     id__in=[item.id for item in
                                                                                             estimated_recurring_transactions(
                                                                                                 False, request.user)])
        estimated_recurring_month_sum = \
            estimated_recurring_transactions_month.exclude(value__lte=0).aggregate(Sum('value'))[
                'value__sum'] or 0
        month_current_sum = \
            app.utils.expenses_transactions(request.user).filter(date__gte=start_month, date__lte=end_month).aggregate(
                Sum('value'))['value__sum'] or 0
        month_expected_sum = month_current_sum + estimated_recurring_month_sum

        estimated_recurring_transactions_bill_month = RecurringTransaction.objects.filter(user=request.user,
                                                                                          id__in=[item.id for item in
                                                                                                  estimated_recurring_transactions(
                                                                                                      True,
                                                                                                      request.user)])
        estimated_transactions_bill_month_total = estimated_recurring_transactions_bill_month.aggregate(Sum('value'))[
                                                      'value__sum'] or 0
        estimated_total_balance = total_balance - estimated_transactions_bill_month_total

        data = [
            {'key': 'Bank Balance', 'value': bank_balance},
            {'key': 'Account Balance', 'value': total_balance},
            {'key': 'Expected Balance', 'value': round(estimated_total_balance)},
            {'key': 'Expected End Of Month Expenses', 'value': round(month_expected_sum)},
            {'key': 'Average Monthly Income', 'value': avg_monthly_income},
            {'key': 'Average Monthly Expenses', 'value': avg_monthly_expenses}]
        return Response(data)


class UserTransactionsNames(APIView):
    serializer_class = UserTransactionsNamesSerializer
    def get(self, request, format=None):
        transactions = Transaction.objects.filter(user=request.user).values_list('name').distinct()
        return Response(data=transactions)


class TransactionViewSet(viewsets.ModelViewSet):
    serializer_class = TransactionRestSerializer
    queryset = Transaction.objects.none()
    filterset_fields = {
        'date': ['gte', 'lte', 'exact', 'gt', 'lt'],
    }

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return Transaction.objects.none()
        if self.request.GET.get('category'):
            return self.request.user.transaction_set.filter(tag__name=self.request.GET.get('category')).order_by(
                '-date')
        return self.request.user.transaction_set.all().order_by('-date')


class CredentialViewSet(viewsets.ModelViewSet):
    serializer_class = CredentialSerializer
    queryset = Credential.objects.none()

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return Credential.objects.none()
        return Credential.objects.filter(user=self.request.user)


def estimated_recurring_transactions(bill_month, user):
    non_registered_transactions = []
    for item in RecurringTransaction.objects.filter(user=user):
        if bill_month:
            date__in_month = date_in_bill_month(item.date.day, user)
            end = next_bill_date(user)
            start = end - relativedelta(months=1)
        else:
            date__in_month = datetime.date.today().replace(day=min(item.date.day, end_month(datetime.date.today()).day))
            start = datetime.date.today().replace(day=1)
            end = datetime.date.today().replace(day=calendar.monthrange(start.year, start.month)[1])

        min_val, max_val = (item.value * 0.9, item.value * 1.1) if item.value > 0 else (item.value * 1.1, item.value * 0.9)
        if not Transaction.objects.filter(user=user,
                                          name__contains=item.name,
                                          value__lte=max_val,
                                          value__gte=min_val,
                                          date__gte=start,
                                          date__lte=end).exists():
            item.date = date__in_month.date() if isinstance(date__in_month, datetime.datetime) else date__in_month
            non_registered_transactions.append(item)
    return non_registered_transactions
    # return RecurringTransaction.objects.filter(user=user, id__in=non_registered_transactions)


class RecurringTransactionsViewSet(viewsets.ModelViewSet):
    serializer_class = RecurringTransactionSerializer
    queryset = RecurringTransaction.objects.none()

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return RecurringTransaction.objects.none()
        return RecurringTransaction.objects.filter(user=self.request.user)

    def list(self, request, *args, **kwargs):
        return Response(
            RecurringTransactionSerializer(estimated_recurring_transactions(bill_month=True, user=request.user),
                                           many=True).data)


class CredentialTypes(APIView):
    serializer_class = CredentialTypesSerializer
    def get(self, request):
        return Response(models.Credential.COMPANY_CHOICES_WITH_FIELDS)

    def post(self, request):
        data = request.data
        data['user'] = request.user
        m = models.Credential.objects.create(**data)
        return Response(status=201)


class UserView(APIView):
    serializer_class = UserSerializer

    def get(self, request):
        return Response(UserSerializer(request.user).data)


class UserTagViewSet(viewsets.ModelViewSet):
    serializer_class = TagSerializer
    queryset = Tag.objects.none()

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return Tag.objects.none()
        return Tag.objects.filter(user=self.request.user)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        data = serializer.data
        data['goal'] = instance.taggoal_set.first().value if instance.taggoal_set.exists() else None
        transactions_exp = expenses_transactions(instance.user).filter(tag=instance)
        values = transactions_exp.values('month_date').annotate(Sum('value')).order_by('month_date')
        data['expense_month_avg'] = round(sum([v['value__sum'] for v in values]) / len(values)) if values else 0
        data['expense_month_avg'] = round(sum([v['value__sum'] for v in values]) / len(values)) if values else 0
        last_months = list(values)[-4:]
        data['expense_last_months_avg'] = round(
            sum([v['value__sum'] for v in last_months]) / len(last_months)) if last_months else 0
        return Response(data)

    def create(self, request, *args, **kwargs):  # create Goal when creating tag
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        tag = serializer.save()
        goal = request.data['goal']
        models.TagGoal.objects.create(user=request.user, tag=tag, value=goal)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class TotalMonthExpensesView(APIView):
    serializer_class = TotalMonthExpensesSerializer

    def get(self, request, format=None):
        def moving_average(data, window_size):
            moving_average = []
            for i in range(len(data)):
                sum = 0
                for j in range(max(0, i - window_size), i):
                    sum += data[j]
                moving_average.append(sum / window_size)
            return moving_average

        data = []
        start_date = DateInput.objects.filter(user=request.user, name='start_date')
        if start_date.exists():
            transactions_exp = expenses_transactions(request.user)
            # transactions_all = all_transactions_in_dates(request.user)
            if transactions_exp.count() == 0:
                return None
            if request.GET.get('category'):
                transactions_exp = transactions_exp.filter(tag=request.GET.get('category'))
            aggregated_trans = transactions_exp.values('month_date').annotate(Sum('value')).order_by('month_date')
            max_value = aggregated_trans.aggregate(Max('value__sum'))
            min_value = aggregated_trans.aggregate(Min('value__sum'))
            moving_average = moving_average([item['value__sum'] for item in aggregated_trans], 3)
            for i, d in enumerate(aggregated_trans):
                data.append(
                    {
                        'moving_average': moving_average[i],
                        'value': round(d['value__sum']),
                        'text': d['month_date'].strftime("'%y/%m"),
                        'color': get_color(round(d['value__sum']), min_value['value__sum__min'],
                                           max_value['value__sum__max'])
                    }
                )
        return Response(data)


class UserTagGoalView(APIView):
    serializer_class = TagGoalSerializer

    def post(self, request):
        data = request.data
        data['user'] = request.user
        m, created = models.TagGoal.objects.update_or_create(tag_id=data['tag'], defaults={'value': data['value']})
        return Response(data=self.serializer_class(m).data, status=201, ) if created else Response(
            data=self.serializer_class(m).data, status=200)


def add_tag(request):  # TODO: TEST (may not work because tag field was changed to FK)
    TransactionFormSet = formset_factory(TransactionForm, extra=5)
    name = request.POST['fname']
    if name:
        Tag.objects.create(name=name, user=request.user)
    # Get our existing link data for this user.  This is used as initial data.
    # user_links = UserLink.objects.filter(user=user).order_by('anchor')
    link_data = []
    sorted_transaction_formset = TransactionFormSet(form_kwargs={'user': request.user})

    context = {
        'transaction_formset': sorted_transaction_formset
    }
    return render(request, 'pages/tables.html', context)


#######################################################################
# Helper functions
#######################################################################

def get_color(value, min_value, max_value):
    colors = ['#96d3e3', '#6bafc2', '#017fb1', '#01678e', '#015677']

    assert max_value >= min_value
    d = max_value - min_value
    normalized_value = value - min_value
    percent = 100 * normalized_value / d
    return colors[int(percent // 25)]


def create_continuous_day_summery(user):
    start_month = datetime.datetime.now().replace(day=1, minute=0, second=0, microsecond=0)
    end_month = datetime.datetime.now().replace(day=calendar.monthrange(start_month.year, start_month.month)[1],
                                                minute=0, second=0, microsecond=0)
    transactions = Transaction.objects.filter(tag__type=Tag.CONTINUOUS, date__gte=start_month, date__lte=end_month,
                                              user=user)
    date_sums = transactions.values('date').annotate(Sum('value'))
    s=""
    goal = 0
    for date_sum in date_sums:
        t = '\n' + '{} ({}): {}'.format(date_sum['date'].strftime('%d/%m'), date_sum['date'].strftime('%a'),
                                       round(date_sum['value__sum']))

        s += t

    tag_goals = models.TagGoal.objects.filter(tag__type=Tag.CONTINUOUS)
    per_day = round(tag_goals.aggregate(Sum('value'))['value__sum'] / 30)

    s += '\n\n*Goal per day*: {}'.format(round(per_day))

    return s
def create_continuous_category_summery(user):
    start_month = datetime.datetime.now().replace(day=1, minute=0, second=0, microsecond=0)
    end_month = datetime.datetime.now().replace(day=calendar.monthrange(start_month.year, start_month.month)[1],
                                                minute=0, second=0, microsecond=0)
    transactions = Transaction.objects.filter(tag__type=Tag.CONTINUOUS, date__gte=start_month, date__lte=end_month,
                                              user=user)
    tag_sums = transactions.values('tag_id').annotate(Sum('value'))
    total = 0
    # last_scanned = models.DateInput.objects.get(name='last_scanned', user=request.user).date
    s = '*Date {}*\n'.format(datetime.date.today().strftime('%d/%m'))
    for tag_sum in tag_sums:
        tag = Tag.objects.get(id=tag_sum['tag_id'])
        goal = tag.taggoal_set.first()
        if goal:
            diff = int(goal.value) - tag_sum['value__sum']
        else:
            diff = 0
        value_sum = round(tag_sum['value__sum']) if diff >= 0 else '*{}*'.format(round(tag_sum['value__sum']))
        total += diff
        t = '\n' + '{}: {}/ {}'.format(tag.name.replace('_', ' ').capitalize(),
                                       value_sum, str(int(goal.value)) if goal else '')

        s += t
        # add TagGaols with 0 spent
    tag_goals = models.TagGoal.objects.exclude( # TODO FIX so it will not have all the tag names
        tag__name__in=['credit cards', 'bills', 'salary', 'same', 'debt payment', 'Donations', 'other income',
                       'commission', 'exclude', 'vacation'])
    tag_goals = tag_goals.filter(tag__type=Tag.CONTINUOUS).exclude(
        tag__id__in=[tag_sum['tag_id'] for tag_sum in tag_sums]).exclude(
        tag__expense=False)
    for tag_goal in tag_goals:
        if tag_goal.value == 0:
            continue
        t = '\n' + '{}: {}/ {}'.format(tag_goal.tag.name.replace('_', ' ').capitalize(),
                                       str(0), str(int(tag_goal.value)))
        s += t
        total += tag_goal.value

    # add total left
    s += '\n\n*Left*: {}'.format(round(total))

    return s


def load_excel_file(ws, user):
    sorted_transactions = list()
    unsorted_transactions = list()
    # iterating over the rows and
    # getting value from each cell in row
    for row in list(ws.iter_rows()):
        if not row[1].value or not row[3].value or not row[0].value:
            continue
        row_data = {}
        row_data["name"] = row[1].value
        row_data["value"] = row[3].value.replace("₪", "").replace(",", "").strip()
        row_data["date"] = row[0].value
        tag = TransactionNameTag.get_tag(row_data["name"], user)
        if tag:
            row_data["tag"] = tag.name
            sorted_transactions.append(row_data)
        else:
            unsorted_transactions.append(row_data)
    return sorted_transactions + unsorted_transactions


def reformat_figs(data):
    for name, fig in data.items():
        if not fig:
            data[name] = NO_DATA_HTML
        else:
            fig.update_layout(margin=dict(l=0, r=0, t=0, b=0))
            data[name] = fig.to_html(full_html=False, config={'displayModeBar': False})
    return data


class ChatHistoryView(APIView):
    """Return conversation history for the authenticated user."""

    serializer_class = MessageSerializer

    def get(self, request):
        conversation, _ = Conversation.objects.get_or_create(user=request.user)
        messages = conversation.messages.all()
        return Response(MessageSerializer(messages, many=True).data)


class ChatSendView(APIView):
    """Accept a user message and return the agent response."""

    serializer_class = MessageSerializer

    def post(self, request):
        conversation, _ = Conversation.objects.get_or_create(user=request.user)
        text = request.data.get("text", "")
        user_msg = Message.objects.create(
            conversation=conversation,
            sender=Message.USER,
            content_type="text",
            payload={"text": text},
        )

        agent_msg = Message.objects.create(
            conversation=conversation,
            sender=Message.AGENT,
            content_type="text",
            payload={"text": f"Echo: {text}"},
        )
        return Response(MessageSerializer(agent_msg).data)


