# Django
from django.utils.translation import gettext_lazy as _

# Django REST Framework
from rest_framework import serializers

# Models
from warrants.models import Warrant

# Fields
from warrants import fields


class WarrantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Warrant
        fields = '__all__'

    origin_location = fields.CoordinateField()
    destination_location = fields.CoordinateField()

    def validate_status(self, value: str) -> str:
        """
        If the instance is created the status always is created
        """
        if self.instance:
            return value
        else:
            return Warrant.Status.CREATED
