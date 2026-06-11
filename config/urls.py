from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/users/", include("app.api.users.urls")),
    path("api/catalog/", include("app.api.catalog.urls")),
    path("api/orders/", include("app.api.orders.urls")),
    path("api/chatbot/", include("app.api.chatbot.urls")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
