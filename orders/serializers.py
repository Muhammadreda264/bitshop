from rest_framework import serializers
from rest_framework.relations import HyperlinkedIdentityField
from rest_framework_nested.relations import NestedHyperlinkedRelatedField, NestedHyperlinkedIdentityField
from rest_framework_nested.serializers import NestedHyperlinkedModelSerializer

from orders.models import Order, OrderItem


class OrderSerializer(serializers.HyperlinkedModelSerializer):
    items = NestedHyperlinkedRelatedField(
        many=True,
        read_only=True,  # Or add a queryset
        view_name='order-item-detail',
        parent_lookup_kwargs={'order_pk': 'order__pk'}
    )

    total = serializers.ReadOnlyField()

    class Meta:
        model = Order
        fields = '__all__'
        extra_kwargs = {'quantity': {'required': False}, 'user': {"read_only": True}}


class OrderItemSerializer(NestedHyperlinkedModelSerializer):
    total = serializers.ReadOnlyField()
    parent_lookup_kwargs = {
        'order_pk': 'order__pk',
    }
    url = NestedHyperlinkedIdentityField(parent_lookup_kwargs={'order_pk': 'order__pk'}, view_name='order-item-detail')

    class Meta:
        model = OrderItem
        fields = '__all__'
        extra_kwargs = {'quantity': {'required': False},
                        'cart': {"read_only": True}, 'order': {"read_only": True}}
