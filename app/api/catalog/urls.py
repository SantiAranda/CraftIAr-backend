from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CategoryListView, ProductViewSet

router = DefaultRouter()
router.register(r'products', ProductViewSet, basename='products')

urlpatterns = [
    path('categories/', CategoryListView.as_view(), name='category-list'),
    path('', include(router.urls)),
]
