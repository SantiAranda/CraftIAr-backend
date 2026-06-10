from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import OrderViewSet, SubscriptionView, CartSyncView

router = DefaultRouter()
router.register(r'orders', OrderViewSet, basename='orders')

urlpatterns = [
    path('subscription/', SubscriptionView.as_view(), name='subscription'),
    path('cart/sync/', CartSyncView.as_view(), name='cart-sync'),
    path('', include(router.urls)),
]
