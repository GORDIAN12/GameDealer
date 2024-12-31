from django.urls import path
from . import views
urlpatterns=[
    path('', views.index, name='index'),
    path('producto/<int:producto_id>/', views.detail_product, name='detail_product'),
    ]
