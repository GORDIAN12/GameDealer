from django.shortcuts import render,  redirect, reverse
from django.http import HttpResponse
from django.views import View
from .models import Product
import stripe
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.views.generic.base import TemplateView
from django.contrib.auth.decorators import login_required
from django .contrib.auth import authenticate, login, logout 
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm 
from .models import *
from .utils import *

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
            return redirect('shop')
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
    products_list=stripe.Product.list()
    products=[]
    special_product='prod_RhJJK1OMe6aNYj'
    for product in products_list['data']:
        if product.get('metadata', {}).get('category')=="shop":
            products.append(get_product_detail(product)) 
    products=products[:8]
    return render(request, 'index.html', {'products': products, 'special_product': special_product})

def origin(request):
    return render(request, 'origin.html')

def shop(request):
    products = []
    
    has_more = True
    starting_after = None

    while has_more:
        if starting_after:
            products_list = stripe.Product.list(limit=100, starting_after=starting_after)
        else:
            products_list = stripe.Product.list(limit=100)
        
        for product in products_list['data']:
            if product.get('metadata', {}).get('category') == "shop":
                products.append(get_product_detail(product))
        
        has_more = products_list['has_more']
        if has_more:
            starting_after = products_list['data'][-1]['id']  # El ID del último producto en la página

    return render(request, 'shop.html', {'products': products})


def product_view(request, product_id):
    product=product_id
    product=stripe.Product.retrieve(product_id)
    product_details=get_product_detail(product)
    prices=stripe.Price.list(product=product_id)
    price=prices.data[0]
    product_price=price.unit_amount/100.0

    stripe.api_key = settings.STRIPE_SECRET_KEY

    if request.method == 'POST':
        if not request.user.is_authenticated:
            return redirect(f'{settings.BASE_URL}{reverse("login")}?next={request.get_full_path()}')
        price_id = request.POST.get('price_id')
        quantity = int(request.POST.get('quantity', '1'))

        checkout_session = stripe.checkout.Session.create(
                line_items=[
                    {
                        "price": price_id,
                        "quantity": quantity,
                    },
                ],
                payment_method_types = ['card'],
                mode="payment",
                customer_creation = 'always',
                success_url = f'{settings.BASE_URL}{reverse("payment_successful")}?session_id={{CHECKOUT_SESSION_ID}}',
                cancel_url = f'{settings.BASE_URL}{reverse("payment_cancelled")}',
                )
        return redirect(checkout_session.url, code=303)
    return render(request, 'product.html', {'product': product_details, 'price_id': price.id})

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


@require_POST
@csrf_exempt
def stripe_webhook(request):
    endpoint_secret=settings.STRIPE_WEBHOOK_SECRET
    payload = request.body
    signature_header = request.META['HTTP_STRIPE_SIGNATURE']
    event = None
    try:
        event=stripe.Webhhok.construct_event(
            payload, signature_header,endpoint_secret
                )
    except:
        return HttpResponse(status=400)

    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        checkout_session_id = session.get('id')
        user_payment = UserPayment.objects.get(stripe_checkout_id=checkout_session_id)
        user_payment.has_paid = True
        user_payment.save()

    return HttpResponse(status=200)
