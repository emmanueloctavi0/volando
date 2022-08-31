# Django
from django.urls import include, path

# Django REST Framework
from rest_framework import routers

# Views
from orders import views


router = routers.DefaultRouter()
router.register('', views.OrderViewSet)

app_name = 'orders'

urlpatterns = [
    path('', include(router.urls)),
]
