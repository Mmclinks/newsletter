from django.contrib import messages
from django.core.mail import EmailMessage
from django.urls import reverse_lazy
from django.views.generic import FormView, TemplateView

from config.forms.forms import ContactForm
from mailings.models import Client, Mailing


class HomePageView(TemplateView):
    template_name = 'users/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["total_mailings"] = Mailing.objects.count()
        context["active_mailings"] = Mailing.objects.filter(status="Запущена").count()
        context["unique_recipients"] = Client.objects.distinct().count()
        return context


class ContactsView(FormView):
    """
    Представление страницы контактов
    """

    template_name = "contacts.html"
    form_class = ContactForm
    success_url = reverse_lazy("contacts")

    def form_valid(self, form):
        """
        Переопределение метода для отправки письма при успешной отправки формы
        """
        name = form.cleaned_data["name"]
        message = form.cleaned_data["message"]
        subject = f"Новое сообщение от {name}"
        recipient_list = ["lacryk@gmail.com"]

        email = EmailMessage(
            subject=subject,
            body=message,
            from_email="lacryk@yandex.ru",
            to=recipient_list,
        )

        email.headers = {
            "Reply-To": "lacryk@yandex.ru",
        }

        email.send(fail_silently=False)

        messages.success(
            self.request, f'Спасибо, {name}! Ваше сообщение "{message}" получено.'
        )  # Добавляем сообщение об успехе
        return super().form_valid(form)

    def form_invalid(self, form):
        """
        Если форма недействительна, просто отобразим шаблон с ошибками
        """
        return super().form_invalid(form)
