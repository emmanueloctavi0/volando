# Django
from django.urls import reverse
from django.contrib.auth import get_user_model

# GEODjango
from django.contrib.gis.geos import Point

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
