from django import forms

from clients.models import Client
from mailings.models import Mailing
from messages_list.models import Message


class ContactForm(forms.Form):
    """
    Форма страницы контактов
    """
    name = forms.CharField(max_length=100, label="Ваше имя")
    message = forms.CharField(widget=forms.Textarea, label="Ваше сообщение")


class ClientForm(forms.ModelForm):
    """
    Форма создания клиента
    """
    class Meta:
        model = Client
        fields = [
            "full_name",
            "email",
            "comment",
        ]
        widgets = {
            "full_name": forms.TextInput(attrs={"class": "form-control", "placeholder": "Ваше имя"}),
            "email": forms.EmailInput(attrs={"class": "form-control", "placeholder": "Ваша почта"}),
            "comment": forms.Textarea(attrs={"class": "form-control", "placeholder": "Комментарий"}),
        }


class MessageForm(forms.ModelForm):
    """
    Форма создания сообщения
    """
    class Meta:
        model = Message
        fields = ["subject", "body"]
        widgets = {
            "subject": forms.TextInput(attrs={"class": "form-control", "placeholder": "Тема сообщения"}),
            "body": forms.TextInput(attrs={"class": "form-control", "placeholder": "Текст сообщения"}),
        }


class MailingForm(forms.ModelForm):
    """
    Форма создания рассылки
    """
    class Meta:
        model = Mailing
        fields = ["start_time", "end_time", "status", "message", "recipients"]

        widgets = {
            "start_time": forms.DateTimeInput(
                attrs={
                    "type": "datetime-local",
                    "class": "form-control",
                    "placeholder": "Начало",
                }
            ),
            "end_time": forms.DateTimeInput(
                attrs={
                    "type": "datetime-local",
                    "class": "form-control",
                    "placeholder": "Окончание",
                }
            ),
            "status": forms.Select(attrs={"class": "form-control"}),
            "message": forms.Select(attrs={"class": "form-control"}),
            "recipients": forms.SelectMultiple(attrs={"class": "form-control"}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)

        if user:
            self.fields["message"].queryset = Message.objects.filter(owner=user)
            self.fields["recipients"].queryset = Client.objects.filter(owner=user)
