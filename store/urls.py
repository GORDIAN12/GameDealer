from django.urls import path
from .views import ProductLandingPageView
from . import views
urlpatterns=[
    path('', views.index, name='index'),
    path('landing/', ProductLandingPageView.as_view(), name='landing'),
]
