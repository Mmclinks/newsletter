from django.urls import path
from messages_list.apps import MessagesListConfig
from .views import (MessageCreateView, MessageDeleteView, MessageDetailView,
                    MessageListView, MessageUpdateView)

app_name = MessagesListConfig.name

urlpatterns = [
    path("", MessageListView.as_view(), name="message_list"),
    path("<int:pk>/", MessageDetailView.as_view(), name="message_detail"),
    path("create/", MessageCreateView.as_view(), name="message_create"),
    path("<int:pk>/update/", MessageUpdateView.as_view(), name="message_update"),
    path("<int:pk>/delete/", MessageDeleteView.as_view(), name="message_delete"),
]
