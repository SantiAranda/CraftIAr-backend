from django.db import models
from django.contrib.auth.models import User
from catalog.models import Product

class Subscription(models.Model):
    """
    Control de suscripción para habilitar el Tutor Visual IA de forma dinámica.
    """
    PLAN_CHOICES = (
        ('free', 'Gratuito'),
        ('premium', 'Premium (Acceso Tutor Visual IA)'),
    )
    STATUS_CHOICES = (
        ('active', 'Activa'),
        ('cancelled', 'Cancelada'),
        ('expired', 'Expirada'),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='subscription')
    plan = models.CharField(max_length=20, choices=PLAN_CHOICES, default='free')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    start_date = models.DateTimeField(auto_now_add=True)
    end_date = models.DateTimeField(null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} - {self.get_plan_display()} ({self.status})"


class Order(models.Model):
    """
    Pedido realizado en la tienda
    """
    STATUS_CHOICES = (
        ('pending', 'Pendiente de Pago'),
        ('paid', 'Pagado'),
        ('shipped', 'Enviado'),
        ('delivered', 'Entregado'),
        ('cancelled', 'Cancelado'),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    total = models.DecimalField(max_digits=12, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Pedido #{self.id} - {self.user.username} ({self.status})"


class OrderItem(models.Model):
    """
    Ítems específicos de un pedido
    """
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField(default=1)
    price_at_purchase = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.quantity}x {self.product.name} (Pedido #{self.order.id})"
