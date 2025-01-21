from django.urls import path
from . import views
urlpatterns=[
    path('', views.index, name='index'),
    path('origin', views.origin, name='origin'),
    path('home/', views.home, name='home'),
    path('config/', views.stripe_config),
    path('create-checkout-session/', views.create_checkout_session), # new
    path('payment_successful/', views.payment_successful, name='payment_succesful'),
    path('payment_cancelled/', views.payment_cancelled, name='payment_cancelled'),
    ]
