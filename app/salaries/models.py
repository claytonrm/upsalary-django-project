from django.contrib.auth.models import AbstractUser
from django.db import models

from payees.models import Payee


class CustomUser(AbstractUser):
    pass


class Salary(models.Model):
    received_at = models.DateTimeField(auto_now=True)
    amount = models.DecimalField(max_digits=19, decimal_places=2)
    taxes = models.DecimalField(max_digits=19, decimal_places=2, default=0.0)
    user = models.ForeignKey(Payee, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.id}"
