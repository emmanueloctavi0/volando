# Utils
from . import utils

# Django
from django.contrib.auth import get_user_model

# Django REST Framework
from rest_framework import status
from rest_framework.test import APITestCase

# Models
from orders.models import Order
User = get_user_model()


class OrderCreationTests(APITestCase):

    def setUp(self) -> None:
        self.user = utils.sample_user()
        self.client.force_authenticate(self.user)

    def test_create_order(self):
        """
        Ensure we can create a new order object.
        """
        data = utils.get_order_payload()
        response = self.client.post(utils.ORDER_URL, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Order.objects.count(), 1)
        self.assertEqual(Order.objects.get().address, 'Cuahutemoc')

    def test_always_create_with_status_created(self):
        """Ensure always a new order is created
        with the CREATED status
        """
        data = utils.get_order_payload()
        data['status'] = Order.Status.CANCELLED
        response = self.client.post(utils.ORDER_URL, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Order.objects.count(), 1)
        self.assertEqual(Order.objects.get().status, Order.Status.CREATED)
