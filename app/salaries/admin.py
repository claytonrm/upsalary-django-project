from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DefaultUserAdmin

from .models import Payee, Salary, CustomUser

@admin.register(CustomUser)
class UserAdmin(DefaultUserAdmin):
    pass


@admin.register(Payee)
class UserAdmin(admin.ModelAdmin):
    fields = ("name", "entry", "birthdate")
    list_display = ("name", "entry", "birthdate")
    readonly_fields = ()


@admin.register(Salary)
class SalaryAdmin(admin.ModelAdmin):
    fields = ("user", "amount", "taxes", "received_at")
    list_display = ("user", "amount", "taxes", "received_at")
    readonly_fields = ("received_at",)
