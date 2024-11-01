# cart/models.py

from django.db import models
from django.contrib.auth.models import User
from product.models import ProductPage, VariantOption
from django.utils import timezone

class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    session_key = models.CharField(max_length=40, null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        if self.user:
            return f"Panier de {self.user.username}"
        return f"Panier {self.id}"

    @property
    def total_price(self):
        return sum(item.total_price for item in self.items.all())

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(ProductPage, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    selected_options = models.ManyToManyField(VariantOption, blank=True)

    def __str__(self):
        return f"{self.quantity} x {self.product.title}"

    @property
    def total_price(self):
        base_price = self.product.price
        additional_price = sum(option.additional_price or 0 for option in self.selected_options.all())
        return (base_price + additional_price) * self.quantity
