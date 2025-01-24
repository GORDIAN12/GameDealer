from django.shortcuts import render,  redirect, reverse
from django.http import HttpResponse
from django.views import View
from .models import Product
import stripe
from django.conf import settings
from django.http.response import JsonResponse # new
from django.views.decorators.csrf import csrf_exempt # new
from django.views.generic.base import TemplateView
from django.contrib.auth.decorators import login_required
from django .contrib.auth import authenticate, login, logout 
stripe.api_key = settings.STRIPE_SECRET_KEY

@login_required
def dashboard(request):
    return render(request, 'registration/dashboard.html', {'section': 'dashboard'})


def stripe_config(request):
    if request.method == 'GET':
        stripe_config = {'publicKey': settings.STRIPE_PUBLIC_KEY}
        return JsonResponse(stripe_config, safe=False)

def index(request):
    products=Product.objects.all()
    return render(request, 'index.html', {'products': products})
def origin(request):
    return render(request, 'origin.html')

def product_view(request):  # new
    product_id='prod_RbbNI5xyHbYIQS'
    product=stripe.Product.retrieve(product_id)
    prices=stripe.Price.list(product=product_id)
    price=prices.data[0]
    product_price=price.unit_amount/100.0
    stripe.api_key = settings.STRIPE_SECRET_KEY
    if request.method == 'POST':
        if not request.user.is_authenticated:
            return redirect(f'{settings.BASE_URL}{reverse("login")}?next={request.get_full_path()}')
        
        if request.method == "POST":
            checkout_session = stripe.checkout.Session.create(
                line_items=[
                    {
                        "price": "price_1QiOAbHI987lTkKBTFCZsNBr",  # enter yours here!!!
                        "quantity": 1,
                    }
                ],
                mode="payment",
                #success_url=request.build_absolute_uri(reverse("payment_succesful")),
                #cancel_url=request.build_absolute_uri(reverse("payment_cancelled")),
                success_url = f'{settings.BASE_URL}{reverse("payment_successful")}?session_id={{CHECKOUT_SESSION_ID}}',
                cancel_url = f'{settings.BASE_URL}{reverse("payment_cancelled")}',
                )
            return redirect(checkout_session.url, code=303)
    return render(request, 'product.html', {'product': product, 'product_price': product_price})

def payment_successful(request):
    return render(request, 'payment_succesful.html')
def payment_cancelled(request):
    return render(request, 'payment_cancelled.html')



