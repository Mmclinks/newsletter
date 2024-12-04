from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

from .views import ContactsView, HomePageView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", HomePageView.as_view(), name="home"),
    path("contacts.html", ContactsView.as_view(), name="contacts"),
    path("clients/", include("clients.urls", namespace="clients")),
    path("mailings/", include("mailings.urls", namespace="mailings")),
    path("messages_list/", include("messages_list.urls", namespace="messages")),
    path("users/", include("users.urls", namespace="users")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
