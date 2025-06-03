
from django.urls import path
from . import views

app_name = 'car'

urlpatterns = [
    path('', views.services, name='services'),
    path('models/<slug:slug>/', views.car_detail, name='car_detail'),
]