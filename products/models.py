from django.db import models


class Product(models.Model):
    name = models.TextField()
    price = models.DecimalField(max_digits=12, decimal_places=2)


class Item(models.Model):
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
    quantity = models.IntegerField(default=1)


    class Meta:
        abstract = True


