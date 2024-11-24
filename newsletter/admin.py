from django.contrib import admin
from guardian.shortcuts import assign_perm
from .models import Newsletter

class NewsletterAdmin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        # Назначаем право на изменение рассылки пользователю, который её создал
        assign_perm('change_newsletter', obj.user, obj)

admin.site.register(Newsletter, NewsletterAdmin)
