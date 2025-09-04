from django.urls import path
from .views import index, register, create_product, product_detail, delete_product, update_product
from django.contrib.auth import views as auth_views

app_name = 'products'

urlpatterns = [
    path('', index, name='index'),
    path('accounts/register/', register, name='register'),
    path('accounts/login/', auth_views.LoginView.as_view(template_name='accounts/login.html'), name='login'),
    path('accounts/logout/', auth_views.LogoutView.as_view(next_page='/'), name='logout'),
    path('create/', create_product, name='create_product'),
    path('detail/<int:id>/', product_detail, name='product_detail'),
    path('delete/<int:id>/', delete_product, name='delete_product'),
    path('update/<int:id>/', update_product, name='update_product')
]