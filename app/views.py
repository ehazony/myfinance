# -*- encoding: utf-8 -*-
"""
License: MIT
Copyright (c) 2019 - present AppSeed.us
"""
from django.contrib.auth.decorators import login_required
from django.forms import formset_factory
from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse
from django.template.defaulttags import register

from app.forms import TransactionForm
from app.graph.graph_api import monthly_average_by_category, line_fig_by_tag_by_month, line_fig_by_month, \
    Tag, \
    bar_fig_by_month, expenses_transactions, scatter, all_transactions_in_dates, average_expenses, average_income, \
    number_of_months, average_bank_expenses
from myFinance.models import Transaction, TransactionNameTag, DateInput

from app.excel_parssers import ExcelParser

NO_DATA_HTML = "<div id=chartContainer style=height: 360px; width: 100%;> No data found</div>"


def load_index_figures(user):
    data = dict()
    transactions_exp = expenses_transactions(user)
    transactions_all = all_transactions_in_dates(user)
    data["month average by catergory"] = monthly_average_by_category(user)
    data["total expenses by month bar"] = bar_fig_by_month(transactions_exp)
    data["all tags by month"] = line_fig_by_tag_by_month(transactions_all)
    # data["total expenses by month line"] = total_by_month_line(user)
    # data["accumelating expenses by month"] = accumelatating_by_month(user)
    data["All Transactions"] = scatter(transactions_all)
    return reformat_figs(data)


def load_tag_figures(user, tag):
    data = dict()
    transaction = Transaction.objects.all().filter(tag_ref=tag, user=user)
    data["Total expenses by month for tag {}".format(tag.name)] = bar_fig_by_month(transaction)
    data["Scatter expenses for {}".format(tag.name)] = scatter(transaction)
    data["Graph expenses for {}".format(tag.name)] = line_fig_by_month(transaction)
    return reformat_figs(data)


def load_transaction_name_figuers(user, name):
    data = dict()
    transaction = Transaction.objects.all().filter(name=name, user=user)
    data["Total expenses by month for transaction name {}".format(name)] = bar_fig_by_month(transaction)
    return reformat_figs(data)


@login_required(login_url="/login/")
def index(request):
    data = load_index_figures(request.user)
    return render(request, "index.html", context={"data": data, "average_expenses": average_expenses(request.user),
                                                  "average_income": average_income(request.user),
                                                  "number_of_months": number_of_months(request.user),
                                                  "average_bank_expenses":average_bank_expenses(request.user)})


@login_required(login_url="/login/")
def pages(request):
    context = {}
    # All resource paths end in .html.
    # Pick out the html file name from the url. And load that template.
    try:
        load_template = request.path.split('/')[-1]
        if 'transaction.html' in request.path:
            return by_name(request)
        if 'tag.html' in request.path:
            return by_tag(request)
        if 'tables.html' in request.path:
            return index1(request)
        template = loader.get_template('pages/' + load_template)
        return HttpResponse(template.render(context, request))

    except:

        template = loader.get_template('pages/error-404.html')
        return HttpResponse(template.render(context, request))


def by_tag(request):
    context = {"taglist": Tag.objects.filter(user=request.user)}
    if request.GET.get('id', None):
        tag = Tag.objects.get(id=request.GET.get('id', None))
        context['graphs'] = load_tag_figures(request.user, tag)
    load_template = request.path.split('/')[1]
    template = loader.get_template('pages/' + load_template)
    return HttpResponse(template.render(context, request))


def by_name(request):
    context = {"namelist": Transaction.objects.filter(user=request.user).values_list('name', flat=True).distinct()}
    if request.GET.get('name', None):
        context['graphs'] = load_transaction_name_figuers(request.user, request.GET.get('name'))
        # context['graphs'] = load_tag_figures(tag)
    load_template = request.path.split('/')[1]
    template = loader.get_template('pages/' + load_template)
    return HttpResponse(template.render(context, request))


def tabels(request):
    if "GET" == request.method:
        TransactionFormSet = formset_factory(TransactionForm, extra=5)

        # Get our existing link data for this user.  This is used as initial data.
        # user_links = UserLink.objects.filter(user=user).order_by('anchor')
        link_data = []
        sorted_transaction_formset = TransactionFormSet(form_kwargs={'user': request.user})

        context = {
            'transaction_formset': sorted_transaction_formset
        }
        return render(request, 'pages/tables.html', context)
    else:
        if len(request.FILES) > 0:
            excel_file = request.FILES["excel_file"]

            sorted_transactions = ExcelParser().parse_excel(excel_file, request.user)
            TransactionFormSet = formset_factory(TransactionForm, extra=0)
            sorted_transaction_formset = TransactionFormSet(initial=sorted_transactions,
                                                            form_kwargs={'user': request.user})

            # unsorted_transaction_formset = TransactionFormSet(initial=unsorted_transactions,
            #                                                   form_kwargs={'user': request.user})
            taglist = Tag.objects.all()
            context = {"taglist": taglist, 'sorted_transaction_formset': sorted_transaction_formset}
            # 'unsorted_transactions_formset': unsorted_transaction_formset}
            return render(request, 'pages/tables_transactions.html', context)
        TransactionFormSet = formset_factory(TransactionForm, extra=0)
        is_bank_statements = True if request.POST.get('is_bank') else False
        s = TransactionFormSet(request.POST, form_kwargs={'user': request.user})
        if s.is_valid():
            for transaction in s.forms:
                if transaction.is_valid():
                    t = Transaction.objects.create(user=request.user, name=transaction.cleaned_data.get('name'),
                                                   value=transaction.cleaned_data.get('value'),
                                                   date=transaction.cleaned_data.get('date'),
                                                   tag=transaction.cleaned_data.get('tag'), bank=is_bank_statements)
                    print("created transaction: {}, with date {} and value {}".format(t.name, t.date, t.value))
                    tag = Tag.objects.get(name=transaction.cleaned_data.get('tag'))
                    tt, created = TransactionNameTag.objects.update_or_create(
                        transaction_name=transaction.cleaned_data.get('name'),
                        user=request.user, defaults={'tag': tag})
                    if created:
                        assert TransactionNameTag.objects.filter(user=tt.user,
                                                                 transaction_name=tt.transaction_name).count() == 1
                    DateInput.objects.filter(user=request.user, name='start_date').update(
                        date=Transaction.objects.filter(user=request.user).order_by('month_date')[0].month_date)
            return render(request, 'pages/tables.html', {})
        taglist = Tag.objects.all()

        context = {"taglist": taglist, 'sorted_transaction_formset': s,
                   'unsorted_transactions_formset': []}
        return render(request, 'pages/tables_transactions.html', context)


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
