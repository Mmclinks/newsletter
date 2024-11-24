from django.db import models

from django.shortcuts import render
from django.contrib.auth.decorators import permission_required
from django.views.decorators.cache import cache_page

# Модель "Получатель рассылки"
class Customer(models.Model):
    email = models.EmailField(unique=True)
    full_name = models.CharField(max_length=255)
    comment = models.TextField()

    def __str__(self):
        return self.full_name

# Модель "Сообщение"
class Message(models.Model):
    subject = models.CharField(max_length=255)
    body = models.TextField()

    def __str__(self):
        return self.subject

# Модель "Попытка рассылки"
class SendAttempt(models.Model):
    SUCCESS = 'Успешно'
    FAILED = 'Не успешно'
    STATUS_CHOICES = [
        (SUCCESS, 'Успешно'),
        (FAILED, 'Не успешно'),
    ]

    datetime = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    server_response = models.TextField()
    newsletter = models.ForeignKey('Newsletter', on_delete=models.CASCADE)

# Модель "Рассылка"

class Newsletter(models.Model):
    CREATED = 'Создана'
    RUNNING = 'Запущена'
    COMPLETED = 'Завершена'
    STATUS_CHOICES = [
        (CREATED, 'Создана'),
        (RUNNING, 'Запущена'),
        (COMPLETED, 'Завершена'),
    ]
    # Переименовываем поле, чтобы избежать конфликта
    statistics = models.ForeignKey('NewsletterStatistics', on_delete=models.CASCADE, related_name='newsletter_statistics')
    start_datetime = models.DateTimeField()
    end_datetime = models.DateTimeField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=CREATED)
    message = models.ForeignKey('Message', on_delete=models.CASCADE)
    recipients = models.ManyToManyField('Customer')

    def __str__(self):
        return f'Рассылка: {self.message.subject} ({self.status})'


class NewsletterStatistics(models.Model):
    # Указываем related_name для обратной связи, чтобы избежать конфликта
    newsletter = models.ForeignKey(Newsletter, on_delete=models.CASCADE, related_name='statistics_set')
    successful_sends = models.IntegerField(default=0)
    failed_sends = models.IntegerField(default=0)
    sent_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Statistics for {self.newsletter.subject}'
