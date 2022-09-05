from django.core.exceptions import ObjectDoesNotExist
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED

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


class CartItemViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list` and `retrieve` actions.
    """

    def get_queryset(self):
        return CartItem.objects.filter(cart=self.kwargs['cart_pk'])

    serializer_class = CartItemSerializer

    def create(self, request, *args, **kwargs):
        """
              Add item to cart
        """
        cart = self.kwargs['cart_pk']
        product = request.data.get('product')
        quantity = request.data.get('quantity', 1)
        print(quantity)
        serializer = CartItemCreateSerializer(data={"product": product,
                                                    "cart": cart,
                                                    "quantity": quantity},
                                              context={'request': request})
        try:
            item = CartItem.objects.get(product=product, cart=cart)
            item.quantity = item.quantity + quantity
            item.save()

        except ObjectDoesNotExist:
            if serializer.is_valid(raise_exception=True):
                item = serializer.save()
        return Response(CartItemSerializer(item, context={'request': request}).data,status=HTTP_201_CREATED)
