from django.contrib import admin

from .models import Mailing, MailingAttempt


@admin.register(Mailing)
class MailingAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "start_time",
        "end_time",
        "status",
        "message",
        "show_recipients",
    )
    list_filter = ("start_time", "end_time", "status")
    search_fields = ("start_time", "status")

    def show_recipients(self, obj):
        """
        Выводит имена первых получателей
        """
        return ", ".join([str(recipient) for recipient in obj.recipients.all()[:3]])

    show_recipients.short_description = "Recipients"  # Название колонки в админке


@admin.register(MailingAttempt)
class MailingAttemptAdmin(admin.ModelAdmin):
    list_display = ("id", "mailing", "attempt_time", "status", "response")
    list_filter = ("mailing", "attempt_time", "status")
    search_fields = ("mailing", "attempt_time", "status")
