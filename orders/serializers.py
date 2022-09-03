from rest_framework import serializers
from orders.models import Order, OrderItem


class OrderSerializer(serializers.HyperlinkedModelSerializer):
    items = serializers.HyperlinkedRelatedField(
        many=True,
        read_only=True,
        view_name='orderitem-detail',
    )
    total = serializers.ReadOnlyField()

    class Meta:
        model = Order
        fields = '__all__'
        extra_kwargs = {'quantity': {'required': False}, 'user': {"read_only": True}}


class OrderItemSerializer(serializers.HyperlinkedModelSerializer):
    total = serializers.ReadOnlyField()

    class Meta:
        model = OrderItem
        fields = '__all__'
        extra_kwargs = {'quantity': {'required': False},
                        'cart': {"read_only": True}}
