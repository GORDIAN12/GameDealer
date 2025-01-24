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
def product(request):
    product_id='prod_RbbNI5xyHbYIQS'
    product=stripe.Product.retrieve(product_id)
    prices=stripe.Price.list(product=product_id)
    price=prices.data[0]
    product_price=price.unit_amount/100.0

    if request.method == 'POST':
        if not request.user.is_authenticated:
            return redirect(f'{settings.BASE_URL}{reverse("login")}?next={request.get_full_path()}')

        price_id = request.POST.get('price_id')
        quantity = int(request.POST.get('quantity'))
        checkout_session = stripe.checkout.Session.create(
            line_items = [
                {
                    'price': price_id,
                    'quantity': quantity,
                },
            ],
            payment_method_types = ['card'],
            mode = 'payment',
            customer_creation = 'always',
            success_url = f'{settings.BASE_URL}{reverse("payment_successful")}?session_id={{CHECKOUT_SESSION_ID}}',
            cancel_url = f'{settings.BASE_URL}{reverse("payment_cancelled")}',
        )
        return redirect(checkout_session.url, code=303)  
    

    return render(request, 'product.html', {'product': product, 'product_price': product_price})

@csrf_exempt
def create_checkout_session(request):
    if request.method == 'GET':
        domain_url = 'http://localhost:8000/'
        stripe.api_key = settings.STRIPE_SECRET_KEY
        try:
            checkout_session = stripe.checkout.Session.create(
                success_url=domain_url + 'payment_successful/',
                cancel_url=domain_url + '',
                payment_method_types=['card'],
                mode='payment',
                line_items=[
                    {
                        'price': 'price_1QiOAbHI987lTkKBTFCZsNBr',
                        'quantity': 1,
                    }
                ],
            )
            return JsonResponse({'sessionId': checkout_session['id']})
        except Exception as e:
            return JsonResponse({'error': str(e)})


def origin(request):
    return render(request, 'origin.html')


def payment_successful(request):
    return render(request, 'payment_succesful.html')
def payment_cancelled(request):
    return render(request, 'payment_cancelled.html')
