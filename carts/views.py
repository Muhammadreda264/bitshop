from django.core.exceptions import ObjectDoesNotExist
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from carts.models import Cart, CartItem
from carts.serializers import CartSerializer, CartItemSerializer, CartItemCreateSerializer


class CartViewSet(viewsets.ReadOnlyModelViewSet):
    """
    This viewset automatically provides `list` and `retrieve` actions.
    """
    queryset = Cart.objects.all()
    serializer_class = CartSerializer

    def get_serializer_class(self):
        if self.action == 'item':
            return CartItemSerializer

        return CartSerializer

    @action(detail=True, methods=['PATCH'])
    def empty(self, request, pk=None):
        cart = self.get_object()
        cart.empty()
        return Response(CartSerializer(cart, context={'request': request}).data)

    @action(detail=True, methods=['post'])
    def item(self, request, pk=None):
        """
        Add item to cart
        """
        cart = self.get_object()
        product = request.data.get('product')
        try:
            item = CartItem.objects.get(product=product, cart=cart.pk)
            quantity = request.data.get('quantity', 1)
            item.quantity = item.quantity + quantity
            item.save()
        except ObjectDoesNotExist:
            print(request.data.get('product'))
            print(cart)
            serializer = CartItemCreateSerializer(data={"product": product, "cart": cart.pk})
            if serializer.is_valid(raise_exception=True):
                serializer.save()
        return Response(CartSerializer(cart, context={'request': request}).data)


class CartItemViewSet(viewsets.ReadOnlyModelViewSet):
    """
    This viewset automatically provides `list` and `retrieve` actions.
    """
    queryset = CartItem.objects.all()
    serializer_class = CartItemSerializer
