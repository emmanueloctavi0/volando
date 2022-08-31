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


class OrderUpdateTests(APITestCase):

    def setUp(self):
        self.user = utils.sample_user()
        self.client.force_authenticate(self.user)
        self.order = utils.sample_order(user=self.user)

    def test_update_order_fields(self):
        """
        Test a order can be update with a correct
        payload
        """
        url = utils.detail_url(self.order.pk)
        data = utils.get_order_payload()

        new_data = {
            'address': 'New address',
            'zipcode': '00000',
            'number_products': 111111,
            'products_size': Order.ProductsSize.SMALL
        }

        data.update(new_data)

        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        updated_order = Order.objects.get(pk=self.order.pk)
        updated_order.address = new_data['address']
        updated_order.zipcode = new_data['zipcode']
        updated_order.number_products = new_data['number_products']
        updated_order.products_size = new_data['products_size']

    def test_update_status_created_to_collected(self):
        """Test a order status can change from
        created to collected
        """
        order = utils.sample_order(user=self.user)
        url = utils.detail_url(order.pk)

        payload = {
            'status': Order.Status.COLLECTED
        }

        response = self.client.patch(url, payload, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        updated_order = Order.objects.get(pk=order.pk)
        updated_order.status = Order.Status.COLLECTED

    def test_update_status_collected_to_in_station(self):
        """Test a order status can change from
        collected to in_station
        """
        order = utils.sample_order(
            status=Order.Status.COLLECTED,
            user=self.user
        )
        url = utils.detail_url(order.pk)

        payload = {
            'status': Order.Status.IN_STATION
        }

        response = self.client.patch(url, payload, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        updated_order = Order.objects.get(pk=order.pk)
        updated_order.status = Order.Status.IN_STATION

    def test_update_status_in_station_to_on_route(self):
        """Test a order status can change from
        in_station to on_route
        """
        order = utils.sample_order(
            status=Order.Status.IN_STATION,
            user=self.user
        )
        url = utils.detail_url(order.pk)

        payload = {
            'status': Order.Status.ON_ROUTE
        }

        response = self.client.patch(url, payload, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        updated_order = Order.objects.get(pk=order.pk)
        updated_order.status = Order.Status.ON_ROUTE

    def test_update_status_on_route_to_delivered(self):
        """Test a order status can change from
        on_route to delivered
        """
        order = utils.sample_order(
            status=Order.Status.ON_ROUTE,
            user=self.user
        )
        url = utils.detail_url(order.pk)

        payload = {
            'status': Order.Status.DELIVERED
        }

        response = self.client.patch(url, payload, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        updated_order = Order.objects.get(pk=order.pk)
        updated_order.status = Order.Status.DELIVERED

    def test_update_status_can_be_cancelled(self):
        """
        Test the status can be cancelled when
        the status is created
        """
        order = utils.sample_order(
            status=Order.Status.CREATED,
            user=self.user
        )
        url = utils.detail_url(order.pk)

        payload = {
            'status': Order.Status.CANCELLED
        }

        response = self.client.patch(url, payload, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        updated_order = Order.objects.get(pk=order.pk)
        updated_order.status = Order.Status.CANCELLED

    def test_status_can_not_be_cancelled_when_is_on_route(self):
        """
        Test the status can not be cancelled when
        the status is on_route
        """
        order = utils.sample_order(
            status=Order.Status.ON_ROUTE,
            user=self.user
        )
        url = utils.detail_url(order.pk)

        payload = {
            'status': Order.Status.CANCELLED
        }

        response = self.client.patch(url, payload, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        updated_order = Order.objects.get(pk=order.pk)
        updated_order.status = Order.Status.ON_ROUTE

    def test_status_can_not_be_cancelled_when_is_delivered(self):
        """
        Test the status can not be cancelled when
        the status is delivered
        """
        order = utils.sample_order(
            status=Order.Status.DELIVERED,
            user=self.user
        )
        url = utils.detail_url(order.pk)

        payload = {
            'status': Order.Status.CANCELLED
        }

        response = self.client.patch(url, payload, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        updated_order = Order.objects.get(pk=order.pk)
        updated_order.status = Order.Status.DELIVERED
