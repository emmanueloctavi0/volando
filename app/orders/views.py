
from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

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
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        Get only the user order or
        all if is a superuser
        """
        queryset = super().get_queryset()
        if self.request.user.is_superuser:
            return queryset
        else:
            return queryset.filter(user=self.request.user)

    def perform_create(self, serializer):
        """If the authenticated user is superuser
        create the order with the user sended.
        otherwise crete the order with the logged user
        """
        if self.request.user.is_superuser and serializer.validated_data.get('user'):
            serializer.save()
        else:
            serializer.save(user=self.request.user)
