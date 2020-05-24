from rest_framework import serializers

from payees.serializers import PayeeSerializer

from .models import Payee, Salary


class SalarySerializer(serializers.ModelSerializer):
    user = PayeeSerializer(many=False)

    class Meta:
        model = Salary
        fields = '__all__'
        read_only_fields = ('id', 'received_at')

    def create(self, validated_data):
        payee_data = validated_data.pop('user')
        existing_payee = self.get_payee(payee_data['entry'])
        if existing_payee is not None:
            self.update_nested_payee(existing_payee, payee_data)
            salary, _ = Salary.objects.update_or_create(user=existing_payee, **validated_data)
            return salary
        new_payee = PayeeSerializer.create(PayeeSerializer(), validated_data=payee_data)
        salary, _ = Salary.objects.update_or_create(user=new_payee, **validated_data)
        return salary

    def update(self, instance, validated_data):
        existing_payee = self.get_payee(entry=instance.user.entry)
        if existing_payee is None:
            salary, _ = Salary.objects.update_or_create(user=instance.user, **validated_data)
            return salary

        self.update_nested_payee(existing_payee, validated_data.pop('user'))

        instance.amount = validated_data['amount']
        instance.taxes = validated_data['taxes']
        instance.save()

        return instance

    def update_nested_payee(self, payee, payee_new_data):
        payee.name = payee_new_data['name']
        payee.birthdate = payee_new_data['birthdate']
        payee.save()

    def get_payee(self, entry):
        try:
            return Payee.objects.get(entry=entry)
        except Payee.DoesNotExist:
            pass


class SalaryAmountSummarySerializer(serializers.Serializer):
    average = serializers.DecimalField(max_digits=19, decimal_places=2)
    highest = serializers.DecimalField(max_digits=19, decimal_places=2)
    lowest = serializers.DecimalField(max_digits=19, decimal_places=2)

    class Meta:
        fields = ('__all__')


class SalaryTaxesSummarySerializer(serializers.Serializer):
    average = serializers.DecimalField(max_digits=19, decimal_places=2)

    class Meta:
        fields = ('__all__')


class SalarySummarySerializer(serializers.Serializer):
    amount = SalaryAmountSummarySerializer()
    taxes = SalaryTaxesSummarySerializer()

    class Meta:
        fields = ("__all__")
