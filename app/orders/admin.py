# Django
from django.contrib.gis import admin

# Models
from orders.models import Order


class OrderAdmin(admin.GISModelAdmin):
    pass


admin.site.register(Order, OrderAdmin)
