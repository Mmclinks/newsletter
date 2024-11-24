from django import forms
from .models import Newsletter, Message, Customer

class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['email', 'full_name', 'comment']

class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['subject', 'body']

class NewsletterForm(forms.ModelForm):
    class Meta:
        model = Newsletter
        fields = ['start_datetime', 'end_datetime', 'message', 'recipients']
