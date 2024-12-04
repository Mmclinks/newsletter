from django.core.exceptions import ObjectDoesNotExist
from django.core.management.base import BaseCommand

from mailings.models import Mailing
from mailings.services import send_mailing


class Command(BaseCommand):
    """
    Кастомная команда для запуска рассылки
    """
    help = "Send a mailing to all recipients."

    def add_arguments(self, parser):
        parser.add_argument("mailing_id", type=int)

    def handle(self, *args, **kwargs):
        mailing_id = kwargs["mailing_id"]
        try:
            mailing = Mailing.objects.get(id=mailing_id)
            send_mailing(mailing)
            self.stdout.write(self.style.SUCCESS(f"Mailing {mailing_id} sent successfully."))
        except ObjectDoesNotExist:
            self.stdout.write(self.style.ERROR(f"Mailing with ID {mailing_id} does not exist."))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"An error occurred: {e}"))
