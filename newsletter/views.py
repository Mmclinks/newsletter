from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Newsletter, Message, Customer
from .forms import NewsletterForm, MessageForm, CustomerForm
from .models import NewsletterStatistics
from django.shortcuts import render
from django.contrib.auth.decorators import permission_required
from django.views.decorators.cache import cache_page
from django.shortcuts import render
from guardian.shortcuts import assign_perm
from .models import Newsletter

from django.contrib.auth.models import User

# Главная страница
def index(request):
    total_newsletters = Newsletter.objects.count()
    active_newsletters = Newsletter.objects.filter(status=Newsletter.RUNNING).count()
    unique_customers = Customer.objects.count()

    return render(request, 'newsletter/index.html', {
        'total_newsletters': total_newsletters,
        'active_newsletters': active_newsletters,
        'unique_customers': unique_customers
    })


# Список рассылок
class NewsletterListView(ListView):
    model = Newsletter
    template_name = 'newsletter/newsletter_list.html'


# Создание рассылки
class NewsletterCreateView(CreateView):
    model = Newsletter
    form_class = NewsletterForm
    template_name = 'newsletter/create_newsletter.html'
    success_url = reverse_lazy('newsletter_list')


# Создание сообщения
class MessageCreateView(CreateView):
    model = Message
    form_class = MessageForm
    template_name = 'newsletter/create_message.html'
    success_url = reverse_lazy('message_list')


# Список сообщений
class MessageListView(ListView):
    model = Message
    template_name = 'newsletter/message_list.html'


# Список клиентов
class CustomerListView(ListView):
    model = Customer
    template_name = 'newsletter/customer_list.html'


# Создание клиента
class CustomerCreateView(CreateView):
    model = Customer
    form_class = CustomerForm
    template_name = 'newsletter/create_customer.html'
    success_url = reverse_lazy('customer_list')




def stats_view(request):
    user_newsletters = NewsletterStatistics.objects.filter(newsletter__user=request.user)
    return render(request, 'stats.html', {'newsletters': user_newsletters})


@permission_required('is_manager')
def manager_view(request):
    # Логика для менеджеров
    return render(request, 'manager_view.html')



@cache_page(60 * 15)  # Кеширование на 15 минут
def my_view(request):
    # Логика представления
    return render(request, 'my_template.html')



def assign_permission_view(request, newsletter_id, username):
    # Получаем рассылку и пользователя по переданным параметрам
    newsletter = Newsletter.objects.get(id=newsletter_id)
    user = User.objects.get(username=username)

    # Назначаем разрешение 'change_newsletter' пользователю
    assign_perm('change_newsletter', user, newsletter)

    return render(request, 'success.html', {'message': 'Разрешение успешно назначено!'})
