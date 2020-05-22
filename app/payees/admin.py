from django.contrib import admin

from .models import Payee


@admin.register(Payee)
class UserAdmin(admin.ModelAdmin):
    fields = ("name", "entry", "birthdate")
    list_display = ("name", "entry", "birthdate")
    readonly_fields = ()
