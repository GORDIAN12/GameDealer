from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.http import HttpResponse
from django.views import View
from .models import Product
import stripe
from django.conf import settings
from django.http.response import JsonResponse # new
from django.views.decorators.csrf import csrf_exempt # new
from django.views.generic.base import TemplateView
from django.contrib.auth.decorators import login_required

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


def payment_successful(request):
    return render(request, 'payment_succesful.html')
def payment_cancelled(request):
    return render(request, 'payment_cancelled.html')

def home(request):
    return render(request, 'home.html')





