from django.urls import path

from mailings.apps import MailingsConfig

from .views import (MailingConfirmSendView, MailingCreateView,
                    MailingDeleteView, MailingDetailView, MailingListView,
                    MailingSendView, MailingStatusUpdateView,
                    MailingStatusView, MailingUpdateView)

app_name = MailingsConfig.name

urlpatterns = [
    path("", MailingListView.as_view(), name="mailing_list"),
    path("<int:pk>/", MailingDetailView.as_view(), name="mailing_detail"),
    path("create/", MailingCreateView.as_view(), name="mailing_create"),
    path("<int:pk>/update/", MailingUpdateView.as_view(), name="mailing_update"),
    path("<int:pk>/delete/", MailingDeleteView.as_view(), name="mailing_delete"),
    path("<int:pk>/send/", MailingSendView.as_view(), name="mailing_send"),
    path("<int:pk>/status/", MailingStatusView.as_view(), name="mailing_status"),
    path(
        "<int:pk>/confirm_send/",
        MailingConfirmSendView.as_view(),
        name="mailing_confirm_send",
    ),
    path(
        "<int:pk>/update-status/",
        MailingStatusUpdateView.as_view(),
        name="mailing_status_update",
    ),
]
