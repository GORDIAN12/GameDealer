from django.urls import path
from . import views
urlpatterns=[
    path('', views.index, name='index'),
    path('origin', views.origin, name='origin'),
    path('producto/<int:producto_id>/', views.detail_product, name='detail_product'),
    path('payment_succesful', views.payment_succesful, name='payment_succesful'),
    path('payment_cancelled', views.payment_cancelled, name='payment_cancelled'),
    
    ]
