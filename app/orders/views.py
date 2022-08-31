
from rest_framework import viewsets
from rest_framework import permissions

# Serializers
from orders.serializers import OrderSerializer

# Models
from orders.models import Order


class OrderViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows Orders to be viewed or edited.
    """
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
