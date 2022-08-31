# Django
from django.urls import reverse
from django.contrib.auth import get_user_model

# GEODjango
from django.contrib.gis.geos import Point


# Django REST Framework
from rest_framework import status
from rest_framework.test import APITestCase

# Models
from orders.models import Order
User = get_user_model()


ORDER_URL = reverse('orders:order-list')


def detail_url(order_id):
    """Return order detail URL"""
    return reverse('orders:order-detail', args=[order_id])


def get_order_payload(**params):
    defaults = {
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
    defaults.update(params)
    return defaults


def sample_order(**params):
    data = get_order_payload(**params)

    if isinstance(data['origin_location'], list):
        data['origin_location'] = Point(data['origin_location'])

    if isinstance(data['destination_location'], list):
        data['destination_location'] = Point(data['destination_location'])

    return Order.objects.create(**data)


def sample_user(**params):
    defaults = {
        "username": "user1",
        "password": "Secret@123"
    }

    defaults.update(**params)
    return User.objects.create_user(**defaults)


class OrderCreationTests(APITestCase):

    def setUp(self) -> None:
        self.user = sample_user()
        self.client.force_authenticate(self.user)

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
        """Ensure always a new order is created
        with the CREATED status
        """
        data = get_order_payload()
        data['status'] = Order.Status.CANCELLED
        response = self.client.post(ORDER_URL, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Order.objects.count(), 1)
        self.assertEqual(Order.objects.get().status, Order.Status.CREATED)


class OrderUpdateTests(APITestCase):

    def setUp(self):
        self.user = sample_user()
        self.client.force_authenticate(self.user)
        self.order = sample_order(user=self.user)

    def test_update_order_fields(self):
        """
        Test a order can be update with a correct
        payload
        """
        url = detail_url(self.order.pk)
        data = get_order_payload()

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
        order = sample_order(user=self.user)
        url = detail_url(order.pk)

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
        order = sample_order(status=Order.Status.COLLECTED, user=self.user)
        url = detail_url(order.pk)

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
        order = sample_order(status=Order.Status.IN_STATION, user=self.user)
        url = detail_url(order.pk)

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
        order = sample_order(status=Order.Status.ON_ROUTE, user=self.user)
        url = detail_url(order.pk)

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
        order = sample_order(status=Order.Status.CREATED, user=self.user)
        url = detail_url(order.pk)

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
        order = sample_order(status=Order.Status.ON_ROUTE, user=self.user)
        url = detail_url(order.pk)

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
        order = sample_order(status=Order.Status.DELIVERED, user=self.user)
        url = detail_url(order.pk)

        payload = {
            'status': Order.Status.CANCELLED
        }

        response = self.client.patch(url, payload, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        updated_order = Order.objects.get(pk=order.pk)
        updated_order.status = Order.Status.DELIVERED
