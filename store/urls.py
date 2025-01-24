from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns=[
    path('', views.index, name='index'),
    path('origin', views.origin, name='origin'),
    path('product/', views.product, name='product'),
    path('config/', views.stripe_config),
    path('create-checkout-session/', views.create_checkout_session),
    path('payment_successful/', views.payment_successful, name='payment_succesful'),
    path('payment_cancelled/', views.payment_cancelled, name='payment_cancelled'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('login/', auth_views.LoginView.as_view(),name='login'),
    path('logout/',  auth_views.LoginView.as_view(), name='logout'),
    ]
