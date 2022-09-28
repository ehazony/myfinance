from rest_framework import serializers

from myFinance.models import Transaction, Tag, Credential


class TransactionSerializer(serializers.ModelSerializer):
    tag_name = serializers.CharField(source='tag.name')
    class Meta:
        model = Transaction
        fields = '__all__'

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'

class CredentialSerializer(serializers.ModelSerializer):
    balance = serializers.ReadOnlyField()
    company = serializers.CharField(source='get_company_display')
    type = serializers.CharField(source='get_type_display')
    class Meta:
        model = Credential
        fields = ('company', 'type', 'last_scanned', 'additional_info', 'balance')
