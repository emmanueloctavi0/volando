
# Django
from django.utils.translation import gettext_lazy as _

# Django REST Framework
from rest_framework import serializers

# GEODJango
from django.contrib.gis.geos import Point


class CoordinateField(serializers.ListField):
    """
    Custom field for Coordinates.
    Show the coordinates as a list [longitude, latitude]
    Validate and convert a coordinates to a Point
    """
    def to_representation(self, value: Point) -> list:
        return value.tuple

    def to_internal_value(self, data: list) -> Point:
        try:
            return Point(data)
        except TypeError:
            raise serializers.ValidationError(_('Invalid geopoint'))
