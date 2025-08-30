from django.urls import path
from .views import index, register
from django.contrib.auth import views as auth_views

app_name = 'products'

urlpatterns = [
    path('', index, name='index'),
    path('accounts/register/', register, name='register'),
    path('accounts/login/', auth_views.LoginView.as_view(template_name='accounts/login.html'), name='login'),
    path('accounts/logout/', auth_views.LogoutView.as_view(next_page='/'), name='logout'),

]