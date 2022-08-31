
from rest_framework import viewsets
from rest_framework import permissions

# Serializers
from warrants.serializers import WarrantSerializer

# Models
from warrants.models import Warrant


class WarrantViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows warrants to be viewed or edited.
    """
    queryset = Warrant.objects.all()
    serializer_class = WarrantSerializer
