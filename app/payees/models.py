from django.db import models


class Payee(models.Model):
    name = models.CharField(max_length=255)
    entry = models.CharField(max_length=14)
    birthdate = models.DateField()

    def __str__(self):
        return f"{self.entry} - {self.name}"
