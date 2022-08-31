# Utils
from datetime import datetime, timezone

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
        fields = "__all__"

    origin_location = fields.CoordinateField()
    destination_location = fields.CoordinateField()

    def validate_status(self, value: str) -> str:
        """
        If the instance is created the status always is created
        The warrant can't be cancelled if it status is
        ON_ROUTE or DELIVERED
        """
        # If update
        if self.instance:
            status = self.instance.status
            if (
                status == Warrant.Status.DELIVERED
                or status == Warrant.Status.ON_ROUTE
            ) and value == Warrant.Status.CANCELLED:

                raise serializers.ValidationError(
                    _("The warrant can't be cancelled")
                )

            return value
        else:
            return Warrant.Status.CREATED

    def save(self, **kwargs):
        """Check if a refund is possible"""
        if (
            self.instance
            and self.validated_data["status"] == Warrant.Status.CANCELLED
        ):
            now = datetime.now(timezone.utc)
            diff_time = now - self.instance.created_at

            if diff_time.seconds / 60 <= 2:
                print("Refunding...")
            else:
                print("A refund is not possible")

        return super().save(**kwargs)
