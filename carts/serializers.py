from rest_framework import serializers

from carts.models import Cart, CartItem


class CartSerializer(serializers.HyperlinkedModelSerializer):
    items = serializers.HyperlinkedRelatedField(
        many=True,
        read_only=True,
        view_name='cartitem-detail',
    )
    total = serializers.ReadOnlyField()

    class Meta:
        model = Cart
        fields = '__all__'


class CartItemSerializer(serializers.HyperlinkedModelSerializer):
    total = serializers.ReadOnlyField()
    class Meta:
        model = CartItem
        fields = '__all__'
        extra_kwargs = {'quantity': {'required': False},'cart':{"read_only":True}}


class CartItemCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = '__all__'
        extra_kwargs = {'quantity': {'required': False}}
