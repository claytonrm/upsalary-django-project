from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    pass


class Payee(models.Model):
    name = models.CharField(max_length=255)
    entry = models.CharField(max_length=14)
    birthdate = models.DateField()

    def __str__(self):
        return f"{self.entry} - {self.name}"


class Salary(models.Model):
    received_at = models.DateTimeField(auto_now_add=True)
    amount = models.DecimalField(max_digits=19, decimal_places=2)
    taxes = models.DecimalField(max_digits=19, decimal_places=2, default=0.0)
    user = models.ForeignKey(Payee, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.amount}"
