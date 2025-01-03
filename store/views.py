from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.views import View
from .models import Product

def index(request):
    products=Product.objects.all()
    return render(request, 'index.html', {'products': products})

def origin(request):
    return render(request, 'origin.html')


def detail_product(request, producto_id):
    producto = get_object_or_404(Product, id=producto_id)
    return render(request, 'detail_product.html', {'producto': producto})
