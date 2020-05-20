from rest_framework import serializers
from .models import Payee, Salary


class PayeeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Payee
        fields = '__all__'
        read_only_fields = ('id',)


class SalarySerializer(serializers.ModelSerializer):
    user = PayeeSerializer(many=False, read_only=True)

    class Meta:
        model = Salary
        fields = '__all__'
        read_only_fields = ('id', 'received_at')
