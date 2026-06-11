from rest_framework import viewsets, status, generics
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone
from .models import Order, Subscription, OrderItem
from .serializers import OrderSerializer, OrderCreateSerializer, SubscriptionSerializer
from app.api.catalog.models import Product
from app.api.users.permissions import HasDynamicPermission, has_custom_permission
from .tasks import send_order_status_change_email

class OrderViewSet(viewsets.ModelViewSet):
    """
    Gestión de pedidos:
    - Autenticado: Listar sus propios pedidos o ventas (alcance 'propios') (RF 1.4, 4.3).
    - Vendedor/Admin (permiso 'pedidos.ver_todos'): Listar todos los pedidos (alcance 'todos').
    - Checkout (POST): Crear pedidos con validación de stock y permiso 'carrito.checkout'.
    """
    def get_serializer_class(self):
        if self.action == 'create':
            return OrderCreateSerializer
        return OrderSerializer

    def get_permissions(self):
        if self.action == 'create':
            self.required_permission = 'carrito.checkout'
            self.required_scope = 'propios'
            return [HasDynamicPermission()]
        elif self.action == 'update_status':
            self.required_permission = 'pedidos.cambiar_estado'
            self.required_scope = 'propios'
            return [HasDynamicPermission()]
        elif self.action in ['list', 'retrieve']:
            # El usuario debe poseer al menos pedidos.ver_propios o pedidos.ver_todos
            if has_custom_permission(self.request.user, 'pedidos.ver_todos', 'propios'):
                self.required_permission = 'pedidos.ver_todos'
            else:
                self.required_permission = 'pedidos.ver_propios'
            self.required_scope = 'propios'
            return [HasDynamicPermission()]
        
        return [IsAuthenticated()]

    def get_queryset(self):
        user = self.request.user
        if not user.is_authenticated:
            return Order.objects.none()
        
        # Verificar si el usuario tiene permiso para ver todos los pedidos
        if has_custom_permission(user, 'pedidos.ver_todos', required_scope='todos'):
            return Order.objects.all().order_by('-created_at')
            
        # Si tiene permisos para ver propios (o ver todos con alcance propio)
        if has_custom_permission(user, 'pedidos.ver_propios', required_scope='propios') or has_custom_permission(user, 'pedidos.ver_todos', required_scope='propios'):
            from django.db.models import Q
            # Pedidos creados por él o pedidos con productos creados por él
            return Order.objects.filter(
                Q(user=user) | Q(items__product__created_by=user)
            ).distinct().order_by('-created_at')

        # Por defecto, el comprador sólo ve sus propias compras
        return Order.objects.filter(user=user).order_by('-created_at')

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        order = serializer.save()
        
        # Serializar la respuesta final con el OrderSerializer detallado
        response_serializer = OrderSerializer(order)
        return Response(response_serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['post'], permission_classes=[HasDynamicPermission])
    def update_status(self, request, pk=None):
        """
        RF 4.2 y RF 7.3: Permite cambiar el estado de un pedido.
        Requiere el permiso dinámico 'pedidos.cambiar_estado'.
        """
        self.required_permission = 'pedidos.cambiar_estado'
        self.required_scope = 'propios'
        
        order = self.get_object()
        new_status = request.data.get('status')
        
        valid_statuses = [choice[0] for choice in Order.STATUS_CHOICES]
        if new_status not in valid_statuses:
            return Response(
                {"error": f"Estado inválido. Los estados válidos son: {', '.join(valid_statuses)}"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        old_status = order.status
        order.status = new_status
        order.save()
        
        # Disparar tarea Celery asíncrona para notificar cambio de estado por email (RF 7.3)
        send_order_status_change_email.delay(order.id, old_status, new_status)
        
        return Response({"status": f"Estado del pedido actualizado a {new_status} con éxito."})


class SubscriptionView(generics.RetrieveUpdateDestroyAPIView):
    """
    RF 4.4: Gestión de Suscripciones (Activación y Cancelación simuladas para el MVP).
    - GET: Retorna la suscripción actual.
    - POST: Activa el plan Premium (asigna automáticamente el perfil 'Tutor Visual IA').
    - DELETE: Cancela/vence el plan Premium (revoca automáticamente el perfil).
    """
    permission_classes = [IsAuthenticated]
    serializer_class = SubscriptionSerializer

    def get_object(self):
        subscription, created = Subscription.objects.get_or_create(
            user=self.request.user,
            defaults={'plan': 'free', 'status': 'active'}
        )
        return subscription

    def post(self, request):
        subscription = self.get_object()
        
        # Simulación de pago y activación del plan Premium
        subscription.plan = 'premium'
        subscription.status = 'active'
        subscription.start_date = timezone.now()
        # Vence en 1 mes por defecto
        subscription.end_date = timezone.now() + timezone.timedelta(days=30)
        subscription.save()

        # El signal en Django (handle_subscription_change) se encargará 
        # de crear el UserProfileAssignment del perfil "Tutor Visual IA"
        serializer = self.get_serializer(subscription)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, *args, **kwargs):
        subscription = self.get_object()
        
        # Simulación de cancelación/baja de suscripción
        subscription.plan = 'free'
        subscription.status = 'expired'
        subscription.end_date = timezone.now()
        subscription.save()

        # El signal revoca el perfil "Tutor Visual IA" automáticamente
        serializer = self.get_serializer(subscription)
        return Response(serializer.data, status=status.HTTP_200_OK)


class CartSyncView(APIView):
    """
    Especificación 8.2: Fusión de Carrito (Login-Persistence).
    Valida y consolida los elementos que el usuario tenía en su carrito local (anónimo).
    Retorna la lista de productos válidos, sus precios actuales y si hay suficiente stock.
    """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        items_data = request.data.get('items', [])
        synchronized_items = []
        total_price = 0
        total_weight = 0

        for item in items_data:
            sku = item.get('sku')
            qty = item.get('quantity', 1)

            try:
                product = Product.objects.get(sku=sku)
                # Validar stock disponible
                valid_qty = min(qty, product.stock)
                
                if valid_qty > 0:
                    item_total = product.price * valid_qty
                    total_price += item_total
                    total_weight += product.weight_kg * valid_qty

                    synchronized_items.append({
                        "product_id": product.id,
                        "sku": product.sku,
                        "name": product.name,
                        "price": float(product.price),
                        "requested_quantity": qty,
                        "allocated_quantity": valid_qty,
                        "weight_kg": float(product.weight_kg),
                        "item_total": float(item_total),
                        "has_sufficient_stock": product.stock >= qty
                    })
            except Product.DoesNotExist:
                # Si el producto con ese SKU ya no existe en el catálogo, se descarta silenciosamente
                continue

        return Response({
            "items": synchronized_items,
            "total_price": float(total_price),
            "total_weight_kg": float(total_weight)
        }, status=status.HTTP_200_OK)

