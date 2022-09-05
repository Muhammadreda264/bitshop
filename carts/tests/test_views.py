from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from carts.models import CartItem


class CartItemsTests(APITestCase):
    fixtures = ["products.json", "users.json", "carts.json"]

    def test_create_cart_item(self):

        url = reverse('cart-item-list', kwargs={'cart_pk': 1})
        data = {'product': 1, 'quantity': 1}
        response = self.client.post(url, data, format='json')
        print(response.json())
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(CartItem.objects.count(), 1)
        self.assertEqual(CartItem.objects.get().quantity, 1)

    def test_create_cart_item_with_no_quantity(self):

        url = reverse('cart-item-list', kwargs={'cart_pk': 1})
        data = {'product': 1}
        response = self.client.post(url, data, format='json')
        print(response.json())
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(CartItem.objects.count(), 1)
        self.assertEqual(CartItem.objects.get().quantity, 1)

    def test_create_cart_item_with_specific_quantity(self):
        """
        Ensure we can create a new account object.
        """
        url = reverse('cart-item-list', kwargs={'cart_pk': 1})
        quantity = 9
        data = {'product': 1, 'quantity': quantity}
        response = self.client.post(url, data, format='json')
        print(response.json())
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(CartItem.objects.count(), 1)
        self.assertEqual(CartItem.objects.get().quantity, quantity)

    def test_create_cart_item_with_wrong_cart_pk(self):

        url = reverse('cart-item-list', kwargs={'cart_pk': 1000})
        quantity = 9
        data = {'product': 1, 'quantity': quantity}
        response = self.client.post(url, data, format='json')
        print(response.json())
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_cart_item_with_product_already_exist(self):

        url = reverse('cart-item-list', kwargs={'cart_pk': 1})
        quantity = 9
        data = {'product': 1, 'quantity': quantity}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(CartItem.objects.count(), 1)
        self.assertEqual(CartItem.objects.get().quantity, quantity)
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(CartItem.objects.count(), 1)
        self.assertEqual(CartItem.objects.get().quantity, quantity*2)



