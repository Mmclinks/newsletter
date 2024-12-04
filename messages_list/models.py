from django.contrib.auth import get_user_model
from django.db import models


class Message(models.Model):
    """
    Модель для сообщения
    """
    objects: models.Manager = models.Manager()
    subject = models.CharField(max_length=255)
    body = models.TextField()
    owner = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name="Сообщения",
        verbose_name="Владелец",
    )

    def __str__(self):
        return self.subject

    def is_owned_by(self, user):
        """
        Проверяет, является ли пользователь владельцем сообщения.
        """
        return self.owner == user

    class Meta:
        verbose_name = "сообщение"
        verbose_name_plural = "сообщения"
