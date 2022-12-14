from rest_framework import viewsets, permissions
from rest_framework.response import Response

from carts.models import Cart
from orders.models import Order, OrderItem
from orders.serializers import OrderSerializer, OrderItemSerializer


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request):
        cart = Cart.objects.get(user=request.user)
        order = Order()
        order = order.save_from_cart(cart)
        cart.empty()
        return Response(OrderSerializer(order, context={'request': request}).data)


class OrderItemViewSet(viewsets.ReadOnlyModelViewSet):
    def get_queryset(self):
        return OrderItem.objects.filter(order=self.kwargs['order_pk'])
    serializer_class = OrderItemSerializer
