# Django
from django.urls import path

# Views
from users import views


app_name = 'users'

urlpatterns = [
    path('login/', views.LoginAuthToken.as_view())
]
