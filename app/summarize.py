import datetime
from collections import defaultdict
from unicodedata import category

from django.db.models import Sum, F, Q, Max, Min

from app.utils import expenses_transactions
from myFinance.models import DateInput, Tag, Transaction


def aggregate_category(user, category):
    def moving_average(data, window_size):
        moving_average = []
        for i in range(len(data)):
            sum = 0
            for j in range(max(0, i - window_size), i):
                sum += data[j]
            moving_average.append(sum / window_size)
        return moving_average

    data = []
    start_date = DateInput.objects.filter(user=user, name='start_date')
    if start_date.exists():
        transactions_exp = expenses_transactions(user)
        if transactions_exp.count() == 0:
            return None
        transactions_exp = transactions_exp.filter(tag=category)
        aggregated_trans = transactions_exp.values('month_date').annotate(Sum('value')).order_by('month_date')
        max_value = aggregated_trans.aggregate(Max('value__sum'))
        min_value = aggregated_trans.aggregate(Min('value__sum'))
        moving_average = moving_average([item['value__sum'] for item in aggregated_trans], 3)
        for i, d in enumerate(aggregated_trans):
            data.append(
                {
                    'category': category.name,
                    'moving_average': round(moving_average[i], 2),
                    'current_value': round(d['value__sum']),
                    'current_month': d['month_date'].strftime("%y/%m"),
                }
            )
    return data


def aggregate_categories(user):
    return [aggregate_category(user, category) for category in Tag.objects.filter(user=user)]


def summarize_aggregate(user):
    data = aggregate_categories(user)
    summary_lines = []

    summary_lines.append("=== Aggregated Categories Summary ===\n")

    for category_data in data:
        if category_data:
            for item in category_data:
                summary_lines.append(f"The expenses for category {item['category']} in {item['current_month']} is {item['current_value']}")
                # summary_lines.append(f"  - Moving Average: {item['moving_average']}")
                # summary_lines.append("  - Monthly Breakdown:")
                # for month_data in item['all_months']:
                #     summary_lines.append(f"      * Month: {month_data['month']}, Value: {month_data['value']}")
                summary_lines.append("")  # Add an empty line for separation

    return "\n".join(summary_lines)

def summarize_transaction(transaction: Transaction):
    return f"{transaction.date} - {transaction.name} - {transaction.value} - {transaction.tag.name}"

def summarize_transactions(transactions):
    return "\n".join([summarize_transaction(transaction) for transaction in transactions])



def save_summary_to_file(summary, filename):
    with open(filename, "w") as f:
        f.write(summary)


