from django.contrib.auth.models import User
from django.db.models import Sum
from rest_framework import serializers

from app.utils import expenses_transactions
from myFinance.models import Transaction, Tag, Credential, TagGoal, RecurringTransaction


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = '__all__'


class RestModelSerializer(serializers.ModelSerializer):

    def create(self, validated_data):
        user = None
        request = self.context.get("request")
        if request and hasattr(request, "user"):
            user = request.user
        validated_data['user'] = user
        return super().create(validated_data)


class TransactionRestSerializer(RestModelSerializer):
    tag_name = serializers.CharField(source='tag.name', read_only=True)

    class Meta:
        model = Transaction
        fields = '__all__'


class UserSerializer(RestModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class TagSerializer(RestModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'


class TagExtendedSerializer(TagSerializer):
    goal = serializers.SerializerMethodField()
    expense_month_avg = serializers.SerializerMethodField()

    def get_goal(self, obj):
        return obj.taggoal_set.first().value if obj.taggoal_set.exists() else None

    def get_expense_month_avg(self, obj):
        transactions_exp = expenses_transactions(obj.user).filter(tag=obj)
        values = transactions_exp.values('month_date').annotate(Sum('value')).order_by('month_date')
        return round(sum([v['value__sum'] for v in values]) / len(values)) if values else 0

    class Meta:
        model = Tag
        fields = '__all__'


class TagGoalSerializer(RestModelSerializer):
    class Meta:
        model = TagGoal
        fields = '__all__'


class CredentialSerializer(RestModelSerializer):
    balance = serializers.ReadOnlyField()
    company = serializers.CharField(source='get_company_display')
    type = serializers.CharField(source='get_type_display')

    class Meta:
        model = Credential
        fields = ('id', 'company', 'type', 'last_scanned', 'additional_info', 'balance')


class RecurringTransactionSerializer(RestModelSerializer):
    class Meta:
        model = RecurringTransaction
        fields = '__all__'


class SummeryWidgetsSerializer(serializers.Serializer):
    graphs = serializers.DictField()
    average_expenses = serializers.FloatField()
    average_income = serializers.FloatField()
    number_of_months = serializers.IntegerField()
    average_bank_expenses = serializers.FloatField()


class MonthTrackingSerializer(serializers.Serializer):
    text = serializers.CharField()


class MonthCategorySerializer(serializers.Serializer):
    category_id = serializers.IntegerField()
    category = serializers.CharField()
    key = serializers.CharField()
    value = serializers.FloatField()
    goal = serializers.IntegerField()
    type = serializers.CharField()
    percent = serializers.FloatField()
    color = serializers.CharField()


class BankInfoSerializer(serializers.Serializer):
    key = serializers.CharField()
    value = serializers.FloatField()


class TotalMonthExpensesSerializer(serializers.Serializer):
    moving_average = serializers.FloatField()
    value = serializers.FloatField()
    text = serializers.CharField()
    color = serializers.CharField()


class UserTransactionsNamesSerializer(serializers.Serializer):
    name = serializers.CharField()


class CredentialTypesSerializer(serializers.Serializer):
    key = serializers.CharField()
    name = serializers.CharField()
    fields = serializers.ListField(child=serializers.DictField())

