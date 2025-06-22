from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('orders/', views.order_list, name='order_list'),
    path('orders/create/', views.create_order, name='order_create'),
    path('admin_panel/', views.admin_panel, name='admin_panel'),
    path('', views.home_redirect, name='home'),
]