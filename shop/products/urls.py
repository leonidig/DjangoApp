from django.urls import path
from .views import (index,
                    register,
                    create_product,
                    product_detail,
                    delete_product,
                    update_product, 
                    cart_add,
                    cart_remove,
                    cart_detail,
                    cart_update,
                    order_detail,
                    checkout,
                    seller_confirm_order,
                    seller_orders,
                    my_orders
                )
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
    path('update/<int:id>/', update_product, name='update_product'),
    path("add/<int:product_id>/", cart_add, name="cart_add"),
    path("remove/<int:item_id>/", cart_remove, name="cart_remove"),
    path('cart_detail/', cart_detail, name='cart_detail'),
    path("cart/update/<int:item_id>/", cart_update, name="cart_update"),
    path("checkout/", checkout, name="checkout"),
    path("order/<int:order_id>/", order_detail, name="order_detail"),
    path("seller/orders/", seller_orders, name="seller_orders"),
    path("seller/order/<int:order_id>/", seller_confirm_order, name="seller_confirm_order"),
    path("my_orders/", my_orders, name="my_orders")

]