# -*- encoding: utf-8 -*-
"""
License: MIT
Copyright (c) 2019 - present AppSeed.us
"""
import calendar
import datetime

from django.db.models import Sum
from django.forms import formset_factory
from django.shortcuts import render
from django.template.defaulttags import register
from rest_framework import viewsets
# from app.excel_parssers import ExcelParser
from rest_framework.response import Response
from rest_framework.views import APIView

from app.forms import TransactionForm
# from app.graph.graph_api import monthly_average_by_category, line_fig_by_tag_by_month, line_fig_by_month, \
#     Tag, \
#     bar_fig_by_month, expenses_transactions, scatter, all_transactions_in_dates, average_expenses, average_income, \
#     number_of_months, average_bank_expenses, monthly_average_by_name
from myFinance import models
from myFinance.models import Transaction, TransactionNameTag, DateInput, Tag
from myFinance.serialisers import TransactionSerializer, TagSerializer
from telegram_bot import telegram_bot_api
from . import date_utils
from .graph import graph_api
from .graph.graph_api import average_income

NO_DATA_HTML = "<div id=chartContainer style=height: 360px; width: 100%;> No data found</div>"


# def load_index_figures(user):
#     data = dict()
#     transactions_exp = expenses_transactions(user)
#     transactions_all = all_transactions_in_dates(user)
#     data["total expenses by month bar"] = bar_fig_by_month(transactions_exp)
#     data["all tags by month"] = line_fig_by_tag_by_month(transactions_all)
#     data["month average by catergory"] = monthly_average_by_category(user)
#     # data["total expenses by month line"] = total_by_month_line(user)
#     # data["accumelating expenses by month"] = accumelatating_by_month(user)
#     data["All Transactions"] = scatter(transactions_all)
#     return reformat_figs(data)
#
#
# def load_tag_figures(user, tag):
#     data = dict()
#     transaction = Transaction.objects.all().filter(tag=tag, user=user)
#     data["Total expenses by month for tag {}".format(tag.name)] = bar_fig_by_month(transaction)
#     data["Scatter expenses for {}".format(tag.name)] = scatter(transaction)
#     data["Graph expenses for {}".format(tag.name)] = line_fig_by_month(transaction)
#     # data["Group by Expenses {}".format(tag.name)] = line_fig_by_name_by_month(transaction)
#     data["Group by Expenses {}".format(tag.name)] = monthly_average_by_name(transaction, user, number_of_months(user))
#     last_moth = transaction.aggregate(Max('month_date'))['month_date__max']
#     data["Last month {}".format(tag.name)] = monthly_average_by_name(transaction.filter(month_date=last_moth), user, 1)
#     return reformat_figs(data)


# def load_transaction_name_figuers(user, name):
#     data = dict()
#     transaction = Transaction.objects.all().filter(name=name, user=user)
#     data["Total expenses by month for transaction name {}".format(name)] = bar_fig_by_month(transaction)
#     return reformat_figs(data)


# @login_required(login_url="/login/")
# def index(request):
#     data = {}
#     start_date = DateInput.objects.filter(user=request.user, name='start_date')
#     if start_date.exists():
#         data = load_index_figures(request.user)
#     return render(request, "index.html",
#                   context={"not_start_date": not start_date.exists(), "graphs": data,
#                            "average_expenses": average_expenses(request.user),
#                            "average_income": average_income(request.user),
#                            "number_of_months": number_of_months(request.user),
#                            "average_bank_expenses": average_bank_expenses(request.user)})


class SummeryWidgetsView(APIView):

    def get(self, request, format=None):
        data = {}
        start_date = DateInput.objects.filter(user=request.user, name='start_date')
        if start_date.exists():
            transactions_exp = graph_api.expenses_transactions(request.user)
            transactions_all = graph_api.all_transactions_in_dates(request.user)
            if transactions_exp.count() == 0:
                return None
            aggregated_trans = transactions_exp.values('month_date').annotate(Sum('value'))
            data = aggregated_trans
            # data = load_index_figures(request.user)

        return Response({"graphs": {"total_expenses_by_month_bar": {'dates': [d['month_date'] for d in data],
                                                                    'series': [d['value__sum'] for d in data]}},
                         "average_expenses": graph_api.average_expenses(request.user),
                         "average_income": average_income(request.user),
                         "number_of_months": graph_api.number_of_months(request.user),
                         "average_bank_expenses": graph_api.average_bank_expenses(request.user)})


# def planing_iniail(user):
#     trans = all_transactions_in_dates(user)
#     trans = trans.values('tag').annotate(value=Sum('value') / number_of_months(user))
#     avgs = [{'tag': Tag.objects.get(id=x['tag']), 'value': x['value']} for x in trans]
#     if trans.count() == 0:
#         return None
#     return avgs


# @login_required(login_url="/login/")
# def planing(request):
#     tags = Tag.objects.filter(user=request.user)
#     extra_forms = tags.count()
#     inital = planing_iniail(request.user)
#     income = expenses = 0
#     for x in inital:
#         tag = x['tag']
#         if tag.expense:
#             expenses += x['value']
#         else:
#             income += x['value']
#     some = income + expenses
#     acumelateing = [some * i for i in range(1, 13)]
#     import plotly.express as px
#     fig = px.line(y=acumelateing, )
#     fig = reformat_figs({'fig': fig})
#
#     PlanFormSet = formset_factory(PlanForm, extra=0)
#     if request.method == 'POST':
#         if 'additems' in request.POST and request.POST['additems'] == 'true':
#             formset_dictionary_copy = request.POST.copy()
#             formset_dictionary_copy['form-TOTAL_FORMS'] = int(formset_dictionary_copy['form-TOTAL_FORMS']) + extra_forms
#             formset = PlanFormSet(formset_dictionary_copy)
#         else:
#             formset = PlanFormSet(request.POST)
#             if formset.is_valid():
#                 pass
#     # return HttpResponseRedirect('/about/contact/thankyou')
#     else:
#         formset = PlanFormSet(initial=inital)
#
#     return render(request, "pages/planing.html",
#                   context={'formset': formset, "average_expenses": average_expenses(request.user),
#                            'graphs': fig,
#                            "average_income": average_income(request.user),
#                            "number_of_months": number_of_months(request.user),
#                            "average_bank_expenses": average_bank_expenses(request.user)})


# @login_required(login_url="/login/")
# def pages(request):
#     context = {}
#     # All resource paths end in .html.
#     # Pick out the html file name from the url. And load that template.
#     try:
#         load_template = request.path.split('/')[-1]
#         if 'transaction.html' in request.path:
#             return by_name(request)
#         if 'tag.html' in request.path:
#             return by_tag(request)
#         if 'tables.html' in request.path:
#             return index1(request)
#         template = loader.get_template('pages/' + load_template)
#         return HttpResponse(template.render(context, request))
#
#     except:
#
#         template = loader.get_template('pages/error-404.html')
#         return HttpResponse(template.render(context, request))


def popup(reuest):
    print("hrere")


# def by_tag(request):
#     tag_list = ['--------'] + list(
#         Tag.objects.filter(user=request.user))
#     context = {"taglist": tag_list}
#     if request.GET.get('id', None):
#         tag = Tag.objects.get(id=request.GET.get('id', None))
#         context['graphs'] = load_tag_figures(request.user, tag)
#     load_template = request.path.split('/')[1]
#     template = loader.get_template('pages/' + load_template)
#     context = {**context, **{"average_expenses": average_expenses(request.user),
#                              "average_income": average_income(request.user),
#                              "number_of_months": number_of_months(request.user),
#                              "average_bank_expenses": average_bank_expenses(request.user)}}
#     return HttpResponse(template.render(context, request))


# def by_name(request):
#     name_list = ['--------'] + list(
#         Transaction.objects.filter(user=request.user).values_list('name', flat=True).distinct())
#     context = {"namelist": name_list}
#     if request.GET.get('name', None):
#         context['graphs'] = load_transaction_name_figuers(request.user, request.GET.get('name'))
#     # context['graphs'] = load_tag_figures(tag)
#     load_template = request.path.split('/')[1]
#     template = loader.get_template('pages/' + load_template)
#     context = {**context, **{"average_expenses": average_expenses(request.user),
#                              "average_income": average_income(request.user),
#                              "number_of_months": number_of_months(request.user),
#                              "average_bank_expenses": average_bank_expenses(request.user)}}
#     return HttpResponse(template.render(context, request))
#

# def tabels(request):
#     if "GET" == request.method:
#         TransactionFormSet = formset_factory(TransactionForm, extra=5)
#
# Get our existing link data for this user.  This is used as initial data.
# user_links = UserLink.objects.filter(user=user).order_by('anchor')
# link_data = []
# sorted_transaction_formset = TransactionFormSet(form_kwargs={'user': request.user})
#
# context = {
#     'transaction_formset': sorted_transaction_formset
# }
# return render(request, 'pages/tables.html', context)
# else:
#     if len(request.FILES) > 0:
#         excel_file = request.FILES["excel_file"]
#         try:
#             sorted_transactions = ExcelParser().parse_excel(excel_file, request.user)
#             if sorted_transactions is None:
#                 return render(request, 'pages/error-404.html', {
#                     'text': "Excel format not recognized."
#                             " Send the excel to effi.efficient@gmail.com and we will do are best to add support for your file."})
#         except:
#             if excel_file.name.endswith('.xls'):
#                 return render(request, 'pages/error-404.html', {
#                     'text': ".xls files extention not supported. Please save your file as .xlsx and try again."})
#             return render(request, 'pages/error-404.html', {'text': "Couldn't load file."})
#         TransactionFormSet = formset_factory(TransactionForm, extra=0)
#         sorted_transaction_formset = TransactionFormSet(initial=sorted_transactions,
#                                                         form_kwargs={'user': request.user})

# unsorted_transaction_formset = TransactionFormSet(initial=unsorted_transactions,
#                                                   form_kwargs={'user': request.user})
#     taglist = Tag.objects.all()
#     context = {"taglist": taglist, 'sorted_transaction_formset': sorted_transaction_formset}
#     # 'unsorted_transactions_formset': unsorted_transaction_formset}
#     return render(request, 'pages/tables_transactions.html', context)
# TransactionFormSet = formset_factory(TransactionForm, extra=0)
# is_bank_statements = True if request.POST.get('is_bank') else False
# s = TransactionFormSet(request.POST, form_kwargs={'user': request.user})
# if s.is_valid():
#     for transaction in s.forms:
#         if transaction.is_valid():
#             t = Transaction.objects.create(user=request.user, name=transaction.cleaned_data.get('name'),
#                                            value=transaction.cleaned_data.get('value'),
#                                            date=transaction.cleaned_data.get('date'),
#                                            tag=transaction.cleaned_data.get('tag'), bank=is_bank_statements)
#             print("created transaction: {}, with date {} and value {}".format(t.name, t.date, t.value))
#             tag = Tag.objects.get(user=request.user, name=transaction.cleaned_data.get('tag'))
#             tt, created = TransactionNameTag.objects.update_or_create(
#                 transaction_name=transaction.cleaned_data.get('name'),
#                 user=request.user, defaults={'tag': tag})
#             if created:
#                 assert TransactionNameTag.objects.filter(user=tt.user,
#                                                          transaction_name=tt.transaction_name).count() == 1
#             DateInput.objects.filter(user=request.user, name='start_date').update(
#                 date=Transaction.objects.filter(user=request.user).order_by('month_date')[0].month_date)
#     return render(request, 'pages/tables.html', {})
# taglist = Tag.objects.all()
#
# context = {"taglist": taglist, 'sorted_transaction_formset': s,
#            'unsorted_transactions_formset': []}
# return render(request, 'pages/tables_transactions.html', context)


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


@register.simple_tag
def query_transform(request, **kwargs):
    updated = request.GET.copy()
    updated.update(kwargs)
    return updated.urlencode()


def reformat_figs(data):
    for name, fig in data.items():
        if not fig:
            data[name] = NO_DATA_HTML
        else:
            fig.update_layout(margin=dict(l=0, r=0, t=0, b=0))
            data[name] = fig.to_html(full_html=False, config={'displayModeBar': False})
    return data


def add_tag(request):  # TODO may not work because tag field was changed to FK
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


from django.urls import reverse_lazy
from .forms import TransactionModelForm
from bootstrap_modal_forms.generic import BSModalFormView


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

    def get(self, request, format=None):
        start_month = datetime.datetime.now().replace(day=1, minute=0, second=0, microsecond=0)
        end_month = datetime.datetime.now().replace(day=calendar.monthrange(start_month.year, start_month.month)[1],
                                                    minute=0, second=0, microsecond=0)
        transactions = Transaction.objects.exclude(
            tag__expense=False).filter(date__gte=start_month, date__lte=end_month,
                                       user=request.user)
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
        tag_goals = models.TagGoal.objects.exclude(
            tag__name__in=['credit cards', 'bills', 'salary', 'same', 'debt payment', 'Donations', 'other income',
                           'commission', 'exclude', 'vacation'])
        tag_goals = tag_goals.exclude(tag__id__in=[tag_sum['tag_id'] for tag_sum in tag_sums]).exclude(
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

        telegram_bot_api.send_message(s)
        return Response(data=tag_sums)


#######################################################################
# Widget views
#######################################################################
def get_color(value, min_value, max_value):
    colors = ['#96d3e3', '#6bafc2', '#017fb1', '#01678e', '#015677']

    assert max_value >= min_value
    d = max_value - min_value
    normalized_value = value - min_value
    percent = 100 * normalized_value / d
    return colors[int(percent // 25)]


# class TotalMonthExpensesView(APIView):
#
#     def get(self, request, format=None):
#         data = []
#         start_date = DateInput.objects.filter(user=request.user, name='start_date')
#         if start_date.exists():
#             transactions_exp = expenses_transactions(request.user)
#             transactions_all = all_transactions_in_dates(request.user)
#             if transactions_exp.count() == 0:
#                 return None
#             aggregated_trans = transactions_exp.values('month_date').annotate(Sum('value'))
#             max_value = aggregated_trans.aggregate(Max('value__sum'))
#             min_value = aggregated_trans.aggregate(Min('value__sum'))
#             for d in aggregated_trans.order_by('month_date'):
#                 data.append(
#                     {
#                         'value': round(d['value__sum']),
#                         # AnswerRef: 'one',
#                         'text': d['month_date'].strftime("'%y/%m"),
#                         # Score: 0,
#                         # RespondentPercentage: 12,
#                         # Rank: 1,
#                         'color': get_color(round(d['value__sum']), min_value['value__sum__min'],
#                                            max_value['value__sum__max'])
#                     }
#                 )
#         return Response(data)


class MonthCategoryView(APIView):

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
        transactions = Transaction.objects.exclude(
            tag__name__in=['Credit Cards', 'Bills', 'Salary', 'Same', 'Debt Payment', 'Donations',
                           'Other Income',
                           'Commission', 'Exclude', 'Vacation']).filter(date__gte=start_month,
                                                                        date__lte=end_month,
                                                                        user=request.user)
        if 'category' in request.GET:
            transactions = transactions.filter(tag__name__in=request.GET['category'])

        tag_sums = transactions.values('tag_id').annotate(Sum('value'))
        for i, tag_sum in enumerate(tag_sums):
            tag = Tag.objects.get(id=tag_sum['tag_id'])
            diff = int(tag.taggoal_set.first().value) - tag_sum['value__sum']
            value_sum = round(tag_sum['value__sum']) if diff >= 0 else '*{}*'.format(round(tag_sum['value__sum']))
            value = round(tag_sum['value__sum'])
            goal = int(tag.taggoal_set.first().value)

            data.append(
                {'category': tag.name, 'key': tag.name, 'value': value, 'goal': goal, 'percent': value / goal * 100,
                 'color': Pas[i % len(Pas)]})
        return Response(data)


class BankInfo(APIView):
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

        start_month = datetime.datetime.now().replace(day=1, minute=0, second=0, microsecond=0)
        end_month = datetime.datetime.now().replace(day=calendar.monthrange(start_month.year, start_month.month)[1],
                                                    minute=0, second=0, microsecond=0)
        transactions = Transaction.objects.exclude(
            tag__name__in=['credit cards', 'bills', 'salary', 'same', 'debt payment', 'Donations',
                           'other income',
                           'commission', 'exclude', 'vacation']).filter(date__gte=start_month,
                                                                        date__lte=end_month,
                                                                        user=request.user)
        now = datetime.datetime.now()
        month_salary = \
        Transaction.objects.filter(user=request.user, tag__name__in=['Salary'], date__gte=date_utils.start_month(now),
                                   date__lte=date_utils.end_month(now)).aggregate(Sum('value'))['value__sum']
        avg_monthly_income = graph_api.average_income(request.user)
        avg_monthly_expenses = graph_api.average_expenses(request.user)
        user_info = models.AdditionalInfo.objects.filter(user=request.user, ).order_by('created_at')[-1]
        bank_balance = user_info.value.get('bank_balance')
        data = [{'key': 'Bank Balance', 'value': bank_balance}, {'key': 'Average Monthly Income', 'value': avg_monthly_income},
                {'key': 'Average Monthly Expenses', 'value': avg_monthly_expenses}]
        return Response(data)


class TransactionViewSet(viewsets.ModelViewSet):
    serializer_class = TransactionSerializer
    filterset_fields = {
        'date': ['gte', 'lte', 'exact', 'gt', 'lt'],
    }

    def get_queryset(self):
        if self.request.GET.get('category'):
            return self.request.user.transaction_set.filter(tag__name=self.request.GET.get('category')).order_by(
                '-date')
        return self.request.user.transaction_set.all().order_by('-date')


class UserTagViewSet(viewsets.ModelViewSet):
    serializer_class = TagSerializer

    def get_queryset(self):
        return Tag.objects.filter(user=self.request.user)
