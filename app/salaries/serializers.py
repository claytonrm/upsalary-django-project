from rest_framework import serializers

from payees.serializers import PayeeSerializer

from .models import Salary


class SalarySerializer(serializers.ModelSerializer):
    user = PayeeSerializer(many=False)

    class Meta:
        model = Salary
        fields = '__all__'
        read_only_fields = ('id', 'received_at')

    def create(self, validated_data):
        user = PayeeSerializer.create(PayeeSerializer(), validated_data=validated_data.pop('user'))
        salary, created = Salary.objects.update_or_create(user=user, **validated_data)
        return salary
