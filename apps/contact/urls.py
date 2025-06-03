from django.urls import path
from . import views

app_name = 'contact'

urlpatterns = [
    path('contact-modal/', views.contact_modal, name='contact_modal'),
]