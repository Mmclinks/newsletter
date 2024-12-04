import secrets

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.views import LoginView
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.views import View
from django.views.generic import DetailView, ListView
from django.views.generic.edit import CreateView, UpdateView

from config.settings import EMAIL_HOST_USER

from .forms import CustomUserCreationForm, UserProfileForm
from .models import CustomUser


class RegisterView(CreateView):
    """
    Представление регистрации пользователя
    """
    template_name = "users/register.html"
    form_class = CustomUserCreationForm
    success_url = reverse_lazy("home")

    def form_valid(self, form):
        user = form.save()
        user.is_active = False
        token = secrets.token_hex(16)
        user.token = token
        user.save()
        host = self.request.get_host()
        url = f"http://{host}/users/confirm-registration/{token}/"
        send_mail(
            subject="Подтверждение регистрации на Perfect Mailing",
            message=f"Здравствуйте! Для подтверждения регистрации перейдите по ссылке: {url}",
            from_email=EMAIL_HOST_USER,
            recipient_list=[user.email],
        )

        messages.success(
            self.request,
            "Вы успешно зарегистрировались! Проверьте вашу почту для подтверждения регистрации."
        )
        return super().form_valid(form)


def email_verification(request, token):
    user = get_object_or_404(CustomUser, token=token)
    user.is_active = True
    user.save()
    return redirect(reverse("users:login"))


class CustomLoginView(LoginView):
    """
    Представление для входа
    """
    template_name = "users/login.html"
    success_url = reverse_lazy("catalog:home")


class ProfileView(LoginRequiredMixin, DetailView):
    """
    Представление для просмотра профайла
    """
    model = CustomUser
    form_class = UserProfileForm
    template_name = "users/profile.html"


class ProfileEditView(LoginRequiredMixin, UpdateView):
    """
    Представление для редактирования профайла
    """
    model = CustomUser
    form_class = UserProfileForm
    template_name = "users/edit_profile.html"
    success_url = reverse_lazy("home")

    def get_object(self, queryset=None):
        return self.request.user


class BlockUserView(LoginRequiredMixin, UserPassesTestMixin, View):
    """
    Представление для блокировки пользователей
    """
    def test_func(self):
        # Проверка, что пользователь является менеджером
        return self.request.user.is_staff

    def post(self, request, user_id):
        user = get_object_or_404(CustomUser, id=user_id)
        user.is_active = False
        user.save()
        return redirect("users:user_list")


class UsersListView(ListView):
    """
    Представление списка пользователй
    """
    model = CustomUser
    template_name = "users/users_list.html"
    context_object_name = "users"


class ActivateUserView(UserPassesTestMixin, View):
    """
    Представление для активации пользователя
    """
    def test_func(self):
        return self.request.user.groups.filter(name="Managers").exists()

    def post(self, request, pk):
        user = get_object_or_404(CustomUser, pk=pk)
        user.is_active = True
        user.save()
        messages.success(request, f"Пользователь {user.username} был активирован.")
        return redirect("users:users_list")


class DeactivateUserView(UserPassesTestMixin, View):
    """
    Представление для деактивации пользователя
    """
    def test_func(self):
        return self.request.user.groups.filter(name="Managers").exists()

    def post(self, request, pk):
        user = get_object_or_404(CustomUser, pk=pk)
        user.is_active = False
        user.save()
        messages.success(request, f"Пользователь {user.username} был деактивирован.")
        return redirect("users:users_list")
