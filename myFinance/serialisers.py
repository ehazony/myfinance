from rest_framework import serializers

from myFinance.models import Transaction


class TransactionSerializer(serializers.ModelSerializer):
    tag = serializers.CharField(source='tag.name')
    class Meta:
        model = Transaction
        fields = '__all__'
