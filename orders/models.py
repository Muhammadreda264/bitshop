from django.contrib.auth.models import User
from django.db import models

from products.models import Item, Product


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
    total = models.DecimalField(max_digits=12, decimal_places=2)

    def save_from_cart(self, cart):
        self.total = cart.total
        self.user = cart.user
        self.save()
        cart_items = cart.items.all()
        for cart_item in cart_items:
            OrderItem(quantity=cart_item.quantity, order=self, product=cart_item.product, total=cart_item.total).save()
        return self


class OrderItem(Item):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,

    )
    total = models.DecimalField(max_digits=12, decimal_places=2)
