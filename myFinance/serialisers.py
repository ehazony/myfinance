from django.contrib.auth.models import User
from rest_framework import serializers

from myFinance.models import Transaction, Tag, Credential, TagGoal


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
        fields = ('company', 'type', 'last_scanned', 'additional_info', 'balance')
