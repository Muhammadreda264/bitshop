from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter, SimpleRouter
from rest_framework_nested import routers


from carts.views import CartItemViewSet, CartViewSet
from orders.views import OrderViewSet, OrderItemViewSet
from products.views import ProductViewSet
from users.views import UserViewSet, LoginView

router = DefaultRouter()
router.register(r'products', ProductViewSet, basename="product")
router.register(r'cart-items', CartItemViewSet, basename="cartitem")
router.register(r'carts', CartViewSet, basename="cart")
router.register(r'orders', OrderViewSet, basename="order")
orders_router = routers.NestedSimpleRouter(
    router,
    r'orders',
    lookup='order')
orders_router.register(
    r'items',
    OrderItemViewSet,
    basename='order-item'
)

router.register(r'users', UserViewSet, basename="user")

urlpatterns = [
    path('', include(router.urls)),
    path('', include(orders_router.urls)),
    path('login/', LoginView.as_view()),
    path('admin/', admin.site.urls),
]

