from rest_framework import serializers

from .models import Payee


class PayeeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Payee
        fields = '__all__'
        read_only_fields = ('id',)
