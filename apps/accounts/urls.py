from django.urls import path, include
from . import views
from django.contrib.auth.views import LogoutView

app_name = 'accounts'

urlpatterns = [
    path('auth/', views.auth, name='auth'),
    path('profile/', views.profile_dashboard, name='profile'),
    path('profile/update/', views.profile_update, name='profile_update'),
    path('logout/', LogoutView.as_view(next_page='/'), name='logout'),
    path('', include('django.contrib.auth.urls')),  # Для сброса пароля и других стандартных функций
]
