from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DefaultUserAdmin

from .models import CustomUser, Salary


@admin.register(CustomUser)
class UserAdmin(DefaultUserAdmin):
    pass


@admin.register(Salary)
class SalaryAdmin(admin.ModelAdmin):
    fields = ("user", "amount", "taxes", "received_at")
    list_display = ("user", "amount", "taxes", "received_at")
    readonly_fields = ("received_at",)
