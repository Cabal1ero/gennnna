
from django.urls import path
from . import views


urlpatterns = [
    path('cars/<int:car_id>/order/', views.order_car, name='order_car'),
    path('cancel_order/', views.cancel_order, name='cancel_order'),
]