# Django REST Framework
from rest_framework import serializers

# Models
from warrants.models import Warrant


class WarrantSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Warrant
        fields = '__all__'
