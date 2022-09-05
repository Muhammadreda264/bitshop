from rest_framework import serializers
from rest_framework.relations import PrimaryKeyRelatedField
from rest_framework_nested.relations import NestedHyperlinkedRelatedField, NestedHyperlinkedIdentityField
from rest_framework_nested.serializers import NestedHyperlinkedModelSerializer

from carts.models import Cart, CartItem
from products.models import Product


class CartSerializer(serializers.HyperlinkedModelSerializer):
    items = NestedHyperlinkedRelatedField(
        many=True,
        read_only=True,  # Or add a queryset
        view_name='cart-item-detail',
        parent_lookup_kwargs={'cart_pk': 'cart__pk'}
    )
    total = serializers.ReadOnlyField()

    class Meta:
        model = Cart
        fields = '__all__'


class CartItemSerializer(NestedHyperlinkedModelSerializer):
    total = serializers.ReadOnlyField()
    parent_lookup_kwargs = {'cart_pk': 'cart__pk'}
    url = NestedHyperlinkedIdentityField(parent_lookup_kwargs={'cart_pk': 'cart__pk'}, view_name='cart-item-detail')

    class Meta:
        model = CartItem
        fields = '__all__'
        extra_kwargs = {'quantity': {'required': False}, 'cart': {"read_only": True}}


class CartItemCreateSerializer(serializers.ModelSerializer):
    product =PrimaryKeyRelatedField(queryset=Product.objects.all())

    class Meta:
        model = CartItem
        fields = '__all__'
        extra_kwargs = {'quantity': {'required': False}, }
