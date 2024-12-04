from django.contrib.auth import get_user_model
from django.db import models

from clients.models import Client
from messages_list.models import Message


class Mailing(models.Model):
    """
    Модель для рассылок
    """
    objects: models.Manager = models.Manager()
    STATUS_CHOICES = [
        ("Создана", "Создана"),
        ("Запущена", "Запущена"),
        ("Завершена", "Завершена"),
    ]

    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="Создана")
    message = models.ForeignKey(Message, on_delete=models.CASCADE)
    recipients = models.ManyToManyField(Client)
    owner = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name="Рассылки",
        verbose_name="Владелец",
    )

    def __str__(self):
        return f"Рассылка {self.id} ({self.status})"

    def is_owned_by(self, user):
        """Проверяет, является ли пользователь владельцем рассылки."""
        return self.owner == user

    class Meta:
        verbose_name = "рассылка"
        verbose_name_plural = "рассылки"
        permissions = [("can_disable_mailing", "Can disable mailing")]


class MailingAttempt(models.Model):
    """
    Модель для попыток рассылок
    """
    objects: models.Manager = models.Manager()
    STATUS_CHOICES = [
        ("Успешно", "Успешно"),
        ("Не успешно", "Не успешно"),
    ]

    mailing = models.ForeignKey(Mailing, on_delete=models.CASCADE)
    recipient = models.ForeignKey(Client, on_delete=models.CASCADE)
    attempt_time = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    response = models.TextField()

    def __str__(self):
        return f"Попытка {self.id} для рассылки {self.mailing.id}"

    class Meta:
        verbose_name = "попытка рассылки"
        verbose_name_plural = "попытки рассылок"
