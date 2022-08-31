# Django
from django.contrib import admin
from django.urls import include, path

# Django REST Framework
from rest_framework import routers

# Views
from warrants import views


router = routers.DefaultRouter()
router.register(r'warrants', views.WarrantViewSet)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(router.urls)),
]
