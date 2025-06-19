
from django.urls import path
from . import views

app_name = 'order'
urlpatterns = [
    path('cars/<int:car_id>/order/', views.order_car, name='order_car'),
    path('cancel_order/<int:order_id>/', views.cancel_order, name='cancel_order'),
]