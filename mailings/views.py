from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.cache import cache_page
from django.views.generic import (CreateView, DeleteView, DetailView, ListView,
                                  UpdateView)

from config.forms.forms import MailingForm
from .mixins import OwnerOrManagerMixin, OwnerMixin

from .models import Mailing, MailingAttempt
from .services import send_mailing


def send_mailing_view(request, pk):
    mailing = get_object_or_404(Mailing, pk=pk)
    send_mailing(mailing)

    return redirect(reverse("mailings:mailing_status", args=[pk]))


class MailingListView(LoginRequiredMixin, ListView):
    """
    Представление списка всех рассылок
    """
    model = Mailing
    template_name = "mailings/mailings_list.html"
    context_object_name = "mailings"

    def get_queryset(self):
        # Проверяем, принадлежит ли пользователь к группе "менеджеров"
        if self.request.user.groups.filter(name="Managers").exists():
            # Если принадлежит к группе "менеджеры", показываем все клиенты
            return Mailing.objects.all()
        else:
            # Если не принадлежит, показываем только клиенты текущего пользователя
            return Mailing.objects.filter(owner=self.request.user)


class MailingStatusUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """
    Представление для изменения статуса рассылки
    """
    model = Mailing
    fields = []  # Поля для изменения из формы
    template_name = "mailings/mailing_status_update.html"

    def test_func(self):
        # Только менеджеры имеют доступ
        return self.request.user.groups.filter(name="Managers").exists()

    def post(self, request, *args, **kwargs):
        mailing = get_object_or_404(Mailing, pk=self.kwargs["pk"])
        action = request.POST.get("action")

        if action == "activate":
            mailing.status = "Запущена"
            messages.success(request, f"Рассылка '{mailing}' успешно запущена.")
        elif action == "deactivate":
            mailing.status = "Завершена"
            messages.success(request, f"Рассылка '{mailing}' успешно завершена.")
        mailing.save()
        return redirect("mailings:mailing_list")


@method_decorator(cache_page(60 * 15), name='dispatch')
class MailingDetailView(LoginRequiredMixin, OwnerOrManagerMixin, DetailView):
    """
    Представление просмотра рассылки
    """
    model = Mailing
    template_name = "mailings/mailings_detail.html"

    def test_func(self):
        mailing = get_object_or_404(Mailing, id=self.kwargs["pk"])
        return mailing.owner == self.request.user or self.request.user.groups.filter(name="Managers").exists()

    def handle_no_permission(self):
        raise Http404("У вас нет доступа к этой рассылке.")


class MailingCreateView(CreateView):
    """
    Представление для создания рассылки
    """
    model = Mailing
    form_class = MailingForm
    template_name = "mailings/mailing_form.html"
    success_url = reverse_lazy("mailings:mailing_list")

    def get_form_kwargs(self):
        """Передаём пользователя в форму через kwargs."""
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user  # Добавляем текущего пользователя
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["is_update"] = False  # Для создания рассылки
        return context

    def form_valid(self, form):
        # Устанавливаем владельцем текущего пользователя
        form.instance.owner = self.request.user
        return super().form_valid(form)


class MailingUpdateView(LoginRequiredMixin, OwnerMixin, UpdateView):
    """
    Представление для изменения рассылки
    """
    model = Mailing
    form_class = MailingForm
    template_name = "mailings/mailing_form.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["is_update"] = True  # Для редактирования клиента
        return context

    def get_form_kwargs(self):
        """Передаём пользователя в форму через kwargs."""
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user  # Добавляем текущего пользователя
        return kwargs

    def test_func(self):
        mailing = get_object_or_404(Mailing, id=self.kwargs["pk"])
        return mailing.owner == self.request.user

    def handle_no_permission(self):
        raise Http404("У вас нет доступа к этой рассылке.")

    def get_success_url(self):
        """
        Переопределение метода редиректа после успешного изменения статьи
        """
        return reverse("mailings:mailing_detail", kwargs={"pk": self.object.pk})


class MailingConfirmSendView(DetailView):
    """
    Представление для подтверждения запуска рассылки
    """
    model = Mailing
    template_name = "mailings/mailing_confirm_send.html"


class MailingDeleteView(LoginRequiredMixin, OwnerMixin, DeleteView):
    """
    Представление для удаления рассылки
    """
    model = Mailing
    template_name = "mailings/mailings_confirm_delete.html"
    success_url = reverse_lazy("mailings_list")

    def test_func(self):
        mailing = get_object_or_404(Mailing, id=self.kwargs["pk"])
        return mailing.owner == self.request.user

    def handle_no_permission(self):
        raise Http404("У вас нет доступа к этой рассылке.")


class MailingSendView(View):
    """
    Представление для запуска рассылки
    """
    def get(self, request, pk):
        mailing = get_object_or_404(Mailing, pk=pk)

        # Проверка статуса перед отправкой
        if mailing.status == "Запущена":
            messages.warning(request, "Рассылка уже запущена.")
        else:
            send_mailing(mailing)
            mailing.status = "Запущена"
            mailing.save()
            messages.success(request, "Рассылка успешно отправлена.")

        return redirect(reverse("mailings:mailing_status", args=[pk]))


class MailingStatusView(DetailView):
    """
    Представление для страницы статуса рассылки
    """
    model = Mailing
    template_name = "mailings/mailing_status.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Получаем все попытки отправки для данной рассылки
        context["attempts"] = MailingAttempt.objects.filter(mailing=self.object)
        return context


class DisableMailingView(LoginRequiredMixin, UserPassesTestMixin, View):
    """
    Представление для отключения рассылок
    """
    def test_func(self):
        # Проверка, что пользователь является менеджером
        return self.request.user.is_staff

    def post(self, request, mailing_id):
        mailing = get_object_or_404(Mailing, id=mailing_id)
        mailing.status = "Завершена"  # Закрываем рассылку
        mailing.save()
        return redirect("mailings:all_mailings")
