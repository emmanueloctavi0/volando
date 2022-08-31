from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from orders.models import Order


def get_order_payload():
    return {
        'origin_location': [-98.202624, 19.040869],
        'destination_location': [-97.831364, 18.919244],
        'address': 'Cuahutemoc',
        'zipcode': '75420',
        'ext_number': '07',
        'int_number': 'B-311',
        'number_products': 3,
        'products_size': 'LG',
        'status': 'CREATED'
    }

ORDER_URL = reverse('order-list')


class OrderTests(APITestCase):
    def test_create_order(self):
        """
        Ensure we can create a new order object.
        """
        data = get_order_payload()
        response = self.client.post(ORDER_URL, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Order.objects.count(), 1)
        self.assertEqual(Order.objects.get().address, 'Cuahutemoc')

    def test_always_create_with_status_created(self):
        data = get_order_payload()
        data['status'] = Order.Status.CANCELLED
        response = self.client.post(ORDER_URL, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Order.objects.count(), 1)
        self.assertEqual(Order.objects.get().status, Order.Status.CREATED)
