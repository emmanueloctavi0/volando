# Django
from django.utils.translation import gettext_lazy as _

# GEODjango
from django.contrib.gis.db import models

# Models
from volando.models import BaseModel
from django.contrib.auth import get_user_model

User = get_user_model()


class Order(BaseModel):
    origin_location = models.PointField(
        _('Origin coordinates'),
    )

    destination_location = models.PointField(
        _('Destination coordinates')
    )

    address = models.CharField(
        _('Address'),
        max_length=250,
    )

    zipcode = models.CharField(
        _('Zipcode'),
        max_length=100,
    )

    ext_number = models.CharField(
        _('Number'),
        max_length=50,
    )

    int_number = models.CharField(
        _('Internal number'),
        max_length=50,
    )

    number_products = models.IntegerField(
        _('Number of products')
    )

    class ProductsSize(models.TextChoices):
        SMALL = 'SM', _('Small. Max 5kg')
        MEDIUM = 'M', _('Medium. Max 16kg')
        LARGE = 'LG', _('Large. Max 25Kg')

    products_size = models.CharField(
        _('Products size'),
        max_length=5,
        choices=ProductsSize.choices,
    )

    class Status(models.TextChoices):
        CREATED = 'CREATED', _('Created')
        COLLECTED = 'COLLECTED', _('Collected')
        IN_STATION = 'IN_STATION', _('In station')
        ON_ROUTE = 'ON_ROUTE', _('On route')
        DELIVERED = 'DELIVERED', _('Delivered')
        CANCELLED = 'CANCELLED', _('Cancelled')

    status = models.CharField(
        _('Order status'),
        max_length=30,
        choices=Status.choices,
        default=Status.CREATED,
    )

    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    def __str__(self):
        return (
            f'{self.id} - {self.address} '
            f'- {self.status} - {self.created_at}'
        )
