from django.db.models.signals import post_save
from django.dispatch import receiver
from guardian.shortcuts import assign_perm
from .models import Newsletter

@receiver(post_save, sender=Newsletter)
def assign_newsletter_permission(sender, instance, created, **kwargs):
    if created:
        # Назначаем право на изменение рассылки пользователю, который её создал
        assign_perm('change_newsletter', instance.user, instance)
