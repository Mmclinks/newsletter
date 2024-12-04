from django.contrib import admin

from .models import Message


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ("id", "subject", "body")
    list_filter = ("subject",)
    search_fields = ("subject",)