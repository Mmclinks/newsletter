from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    """
    Кастомная команда для создания суперпользователя
    """
    def handle(self, *args, **options):
        User = get_user_model()
        user = User.objects.create(
            email="admin@admin.com",
            first_name="Admin",
            last_name="Full Admin",
        )

        user.set_password("12345")

        user.is_staff = True
        user.is_superuser = True

        user.save()

        self.stdout.write(self.style.SUCCESS(f"Successfully {user.email}"))
