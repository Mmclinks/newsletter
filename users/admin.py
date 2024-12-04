from django.contrib import admin

from users.models import CustomUser


@admin.register(CustomUser)
class UserAdmin(admin.ModelAdmin):
    list_display = ("email", "phone_number")
    search_fields = ("email", "phone_number")
