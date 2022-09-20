from rest_framework import serializers

from myFinance.models import Transaction, Tag


class TransactionSerializer(serializers.ModelSerializer):
    tag = serializers.CharField(source='tag.name')
    class Meta:
        model = Transaction
        fields = '__all__'

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'