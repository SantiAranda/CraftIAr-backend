from rest_framework import viewsets, generics, filters
from rest_framework.permissions import AllowAny, IsAuthenticatedOrReadOnly
from django_filters.rest_framework import DjangoFilterBackend
from .models import Category, Product
from .serializers import CategorySerializer, ProductSerializer
from users.permissions import HasDynamicPermission

class CategoryListView(generics.ListAPIView):
    """
    API pública para listar categorías jerárquicas del catálogo.
    """
    queryset = Category.objects.filter(parent__isnull=True).order_by('name')
    serializer_class = CategorySerializer
    permission_classes = [AllowAny]


class ProductViewSet(viewsets.ModelViewSet):
    """
    ABM de Productos y Catálogo.
    - Lectura pública (GET) para permitir Server-Side Rendering (SSR) en Next.js.
    - Escritura protegida por permisos dinámicos ('catalog:crear' / 'catalog:editar').
    """
    queryset = Product.objects.all().order_by('name')
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['category', 'category__slug']
    search_fields = ['name', 'description', 'sku']
    ordering_fields = ['price', 'name']

    def get_permissions(self):
        # Permitir listado y detalle público para que Next.js pueda indexar vía SSR (RNF 7)
        if self.action in ['list', 'retrieve']:
            return [AllowAny()]
        
        # Operaciones de escritura (crear, modificar, borrar) requieren el permiso correspondiente
        self.required_permission = 'catalog:crear'
        self.required_scope = 'propios'
        return [HasDynamicPermission()]
