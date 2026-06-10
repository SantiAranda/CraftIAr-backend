<<<<<<< HEAD
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

urlpatterns = (
    [
        path("admin/", admin.site.urls),
        path("api/", include("app.api.products.product_url")),
        path("api/", include("app.api.chatbot.chatbot_url")),
    ]
    + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
)
=======
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/users/', include('users.urls')),
    path('api/catalog/', include('catalog.urls')),
    path('api/orders/', include('orders.urls')),
    path('api/chatbot/', include('chatbot.urls')),
]
>>>>>>> origin/feature/integracion-rag
