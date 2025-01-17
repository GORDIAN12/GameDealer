from django.urls import path
from . import views
urlpatterns=[
    path('', views.index, name='index'),
    path('origin', views.origin, name='origin'),
    path('payment_succesful/', views.payment_succesful, name='payment_succesful'),
    path('payment_cancelled/', views.payment_cancelled, name='payment_cancelled'),
    path('home/', views.home, name='home'),
    path('config/', views.stripe_config),  # new
    path('create-checkout-session/', views.create_checkout_session), # new

    ]
