from django.urls import path
from . import views

app_name = 'service'

urlpatterns = [
    path('', views.service_center, name='service_center'),
    path('requests/<int:service_id>/cancel/', views.cancel_service, name='cancel_service'),
] 