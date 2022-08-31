# Django
from django.utils.translation import gettext_lazy as _

# GEODJango
from django.contrib.gis.geos import Point

# Django REST Framework
from rest_framework import serializers

# Models
from warrants.models import Warrant


class WarrantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Warrant
        fields = '__all__'

    def _validate_point(self, value: list) -> Point:
        try:
            return Point(value)
        except TypeError:
            raise serializers.ValidationError(_('Invalid geopoint'))

    def validate_origin_location(self, value: list) -> Point:
        return self._validate_point(value)

    def validate_destination_location(self, value: list) -> Point:
        return self._validate_point(value)

    def save(self, **kwargs):
        # Always save it with the status created
        if not self.instance:
            self.validated_data.update({
                'status': Warrant.Status.CREATED
            })
        return super().save(**kwargs)
