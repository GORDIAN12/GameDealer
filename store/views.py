from django.shortcuts import render,  redirect, reverse
from django.http import HttpResponse
from django.views import View
from .models import Product
import stripe
from django.conf import settings
#from django.http.response import JsonResponse # new
#from django.views.decorators.csrf import csrf_exempt # new
from django.views.generic.base import TemplateView
from django.contrib.auth.decorators import login_required
from django .contrib.auth import authenticate, login, logout 
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm 
from .models import *

stripe.api_key = settings.STRIPE_SECRET_KEY


def register_view(request):
    if request.method=='POST':
        form=UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "cuenta exitosamente creada")
            return redirect('login')
    else:
        form=UserCreationForm()

    return render(request, 'registration/register.html',{'form': form, 'title': 'registro'})

def login_view(request):
    if request.method=='POST':
        username=request.POST.get('username')
        password=request.POST.get('password')
        user=authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('product')
        else:
            messages.error(request, 'usuario o contraseña incorrecto')

    return render(request, 'registration/login.html', {'title': 'inicio sesion',})

def logout_view(request):
        logout(request)
        return redirect('index')

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

        price_id = request.POST.get('price_id')
        checkout_session = stripe.checkout.Session.create(
                line_items=[
                    {
                        "price": 'price_1QiOAbHI987lTkKBTFCZsNBr',  # enter yours here!!!
                        "quantity": 1,
                    },
                ],
                payment_method_types = ['card'],
                mode="payment",
                customer_creation = 'always',
                success_url = f'{settings.BASE_URL}{reverse("payment_successful")}?session_id={{CHECKOUT_SESSION_ID}}',
                cancel_url = f'{settings.BASE_URL}{reverse("payment_cancelled")}',
                )
        return redirect(checkout_session.url, code=303)
    return render(request, 'product.html', {'product': product, 'product_price': product_price})

def payment_successful(request):
    checkout_session_id = request.GET.get('session_id', None)

    if checkout_session_id:
        session = stripe.checkout.Session.retrieve(checkout_session_id)
        customer_id = session.customer
        customer = stripe.Customer.retrieve(customer_id)

        line_item = stripe.checkout.Session.list_line_items(checkout_session_id).data[0]
        UserPayment.objects.get_or_create(
            user = request.user,
            stripe_customer_id = customer_id,
            stripe_checkout_id = checkout_session_id,
            stripe_product_id = line_item.price.product,
            product_name = line_item.description,
            quantity = line_item.quantity,
            price = line_item.price.unit_amount / 100.0,
            currency = line_item.price.currency,
            has_paid = True
        )
    return render(request, 'payment_succesful.html',  {'customer': customer})
def payment_cancelled(request):
    return render(request, 'payment_cancelled.html')



