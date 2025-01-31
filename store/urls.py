from django.urls import path
from . import views
from .views import stripe_webhook, shop
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import LoginView

urlpatterns=[
    path('', views.index, name='index'),
    path('origin', views.origin, name='origin'),
    path('config/', views.stripe_config),
    path('shop/',shop, name="shop"),
    path('product/i<product_id>', views.product_view, name='product'),
    path('payment_successful/', views.payment_successful, name='payment_successful'),
    path('payment_cancelled/', views.payment_cancelled, name='payment_cancelled'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('login/', views.login_view,name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register_view, name='register'),
    path('stripe_webhook/', stripe_webhook, name='stripe_webhook')
    
    ]
