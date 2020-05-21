from rest_framework import serializers
from .models import Payee, Salary

# Movie to Payee app
class PayeeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Payee
        fields = '__all__'
        read_only_fields = ('id',)


class SalarySerializer(serializers.ModelSerializer):
    user = PayeeSerializer(many=False)

    class Meta:
        model = Salary
        fields = '__all__'
        required = ('amo')
        read_only_fields = ('id', 'received_at')

    
    def create(self, validated_data):
        user = PayeeSerializer.create(PayeeSerializer(), validated_data=validated_data.pop('user'))
        salary, created = Salary.objects.update_or_create(user=user, **validated_data)
        return salary