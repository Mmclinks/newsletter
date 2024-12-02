from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404
from django.shortcuts import get_object_or_404
from django.urls import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.generic import (CreateView, DeleteView, DetailView, ListView,
                                  UpdateView)

from config.forms.forms import MessageForm

from .models import Message


class MessageListView(LoginRequiredMixin, ListView):
    """
    Представление списка сообщений
    """
    model = Message
    template_name = "messages_list/message_list.html"
    context_object_name = "messages"

    def get_queryset(self):
        """
        Переопределение метода для проверки является ли пользователь менеджером
        """
        if self.request.user.groups.filter(name="Managers").exists():
            return Message.objects.all().order_by("subject")
        else:
            return Message.objects.filter(owner=self.request.user).order_by("subject")


@method_decorator(cache_page(60 * 15), name='dispatch')
class MessageDetailView(DetailView):
    """
    Представление просмотра сообщения
    """
    model = Message
    template_name = "messages_list/message_detail.html"


class MessageCreateView(CreateView):
    """
    Представление для создания сообщения
    """
    model = Message
    form_class = MessageForm
    template_name = "messages_list/message_form.html"
    success_url = reverse_lazy("messages:message_list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["is_update"] = False  # Для создания клиента
        return context

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class MessageUpdateView(UpdateView):
    """
    Представление для изменения сообщения
    """
    model = Message
    form_class = MessageForm
    template_name = "messages_list/message_form.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["is_update"] = True  # Для редактирования клиента
        return context

    def get_object(self):
        client = get_object_or_404(Message, id=self.kwargs["pk"])
        if not client.is_owned_by(self.request.user):
            raise Http404("Вы не можете редактировать этот клиент.")
        return client

    def test_func(self):
        # Проверка, что пользователь имеет доступ
        return self.get_object().is_owned_by(self.request.user)

    def get_success_url(self):
        """
        Переопределение метода редиректа после успешного изменения статьи
        """
        return reverse("messages:message_detail", kwargs={"pk": self.object.pk})


class MessageDeleteView(DeleteView):
    """
    Представление для удаления сообщения
    """
    model = Message
    template_name = "messages_list/message_confirm_delete.html"
    success_url = reverse_lazy("messages:message_list")
