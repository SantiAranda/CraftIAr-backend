from rest_framework import serializers
from django.db import transaction
from .models import Subscription, Order, OrderItem
from catalog.models import Product
from .tasks import send_order_confirmation_email

class SubscriptionSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = Subscription
        fields = ('id', 'username', 'plan', 'status', 'start_date', 'end_date')


class OrderItemSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.name', read_only=True)
    product_sku = serializers.CharField(source='product.sku', read_only=True)

    class Meta:
        model = OrderItem
        fields = ('id', 'product', 'product_name', 'product_sku', 'quantity', 'price_at_purchase')


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    username = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = Order
        fields = ('id', 'username', 'status', 'total', 'created_at', 'updated_at', 'items')


class OrderCreateItemSerializer(serializers.Serializer):
    product_id = serializers.IntegerField()
    quantity = serializers.IntegerField(min_value=1)


class OrderCreateSerializer(serializers.Serializer):
    items = OrderCreateItemSerializer(many=True, write_only=True)

    def validate_items(self, value):
        if not value:
            raise serializers.ValidationError("Un pedido debe contener al menos un producto.")
        
        # Validar stock disponible para todos los productos en el pedido
        for item in value:
            prod_id = item.get('product_id')
            qty = item.get('quantity')
            try:
                product = Product.objects.get(id=prod_id)
            except Product.DoesNotExist:
                raise serializers.ValidationError(f"El producto con ID {prod_id} no existe.")
            
            if product.stock < qty:
                raise serializers.ValidationError(
                    f"Stock insuficiente para {product.name} (SKU: {product.sku}). Stock disponible: {product.stock}, solicitado: {qty}."
                )
        return value

    def create(self, validated_data):
        user = self.context['request'].user
        items_data = validated_data['items']

        with transaction.atomic():
            # Crear la orden base
            order = Order.objects.create(user=user, total=0, status='pending')
            total = 0

            for item_data in items_data:
                prod_id = item_data.get('product_id')
                qty = item_data.get('quantity')
                
                product = Product.objects.get(id=prod_id)
                
                # Descontar stock
                product.stock -= qty
                product.save()

                price = product.price
                item_total = price * qty
                total += item_total

                # Crear el ítem de la orden
                OrderItem.objects.create(
                    order=order,
                    product=product,
                    quantity=qty,
                    price_at_purchase=price
                )

            # Actualizar el total de la orden
            order.total = total
            order.status = 'paid' # Se marca como pagada para simular el checkout (Límites del sistema: sin pasarela real)
            order.save()

        # Disparar tarea asíncrona de Celery para enviar email de confirmación
        send_order_confirmation_email.delay(order.id)

        return order
