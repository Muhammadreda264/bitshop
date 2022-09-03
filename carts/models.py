from django.contrib.auth.models import User
from django.db import models

from products.models import Product, Item


class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='cart')
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    @property
    def total(self):
        return sum(item.total for item in CartItem.objects.filter(cart=self.pk))

    def empty(self):
        items = self.items.all()
        items.delete()
        return self


class CartItem(Item):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product = models.OneToOneField(
        Product,
        on_delete=models.CASCADE,

    )

    @property
    def total(self):
        return self.quantity * self.product.price
