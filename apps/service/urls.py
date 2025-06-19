from django.urls import path
from . import views

app_name = 'service'

urlpatterns = [
    path('', views.service_center, name='service_center'),
    path('cancel/<int:service_id>/', views.cancel_service, name='cancel_service'),
    path('api/available-times/', views.get_available_times, name='get_available_times'),
]
