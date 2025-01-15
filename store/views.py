from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.views import View
from .models import Product
import stripe
from django.conf import settings

stripe.api_key = settings.STRIPE_SECRET_KEY

def index(request):
    products=Product.objects.all()
    return render(request, 'index.html', {'products': products})

def origin(request):
    return render(request, 'origin.html')
def payment_succesful(request):
    return render(request, 'payment_succesful.html')
def payment_cancelled(request):
    return render(request, 'payment_cancelled.html')




def detail_product(request, producto_id):
    producto = get_object_or_404(Product, id=producto_id)
    product_id='prod_RaT7xZiGNSmeww'
    product=stripe.Product.retrieve(product_id)
    prices=stripe.Price.list(product=product_id)
    price=prices.data[0]
    product_price=price.unit_amount/100.0
    return render(request, 'detail_product.html', {'product': product,'product_price': product_price})
