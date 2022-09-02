from rest_framework import serializers

from products.models import Product


class ProductSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.IntegerField(read_only=True)
    class Meta:
        model = Product
        fields = '__all__'
