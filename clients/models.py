from django.contrib.auth import get_user_model
from django.db import models


class Client(models.Model):
    objects: models.Manager = models.Manager()
    email = models.EmailField(unique=True)
    full_name = models.CharField(max_length=255)
    comment = models.TextField()
    owner = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name="Клиенты",
        verbose_name="Владелец",
    )

    def __str__(self):
        return f"{self.full_name}: {self.email}"

    def is_owned_by(self, user):
        """Проверяет, является ли пользователь владельцем клиента."""
        return self.owner == user

    class Meta:
        verbose_name = "клиент"
        verbose_name_plural = "клиенты"
