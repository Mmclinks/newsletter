from django.contrib import admin

from .models import Client


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ("id", "email", "full_name", "comment")
    list_filter = ("email", "full_name")
    search_fields = ("email", "full_name")
