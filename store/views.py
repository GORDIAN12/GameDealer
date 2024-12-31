import stripe
from django.views.generic import TemplateView  
from django.conf import settings
from django.shortcuts import render
from django.http import HttpResponse
from django.views import View
from .models import Product
stripe.api_key=settings.STRIPE_SECRET_KEY

class succesView(TemplateView):
    template_name="succes.html"

class cancelView(TemplateView):
    template_name="cancel.html"


class ProductLandingPageView(TemplateView):
    template_name="landing.html"

    def get_context_data(self, **kwargs):
        product=Product.objects.get(name="Test Product")
        context=super(ProductLandingPageView, self).get_context_data(**kwargs)
        context.update({
                "product": product,
                "STRIPE_PUBLIC_KEY": settings.STRIPE_PUBLIC_KEY
            })
        return context

class CreateCheckoutSessionView(View):
    def post(self, request, *args, **kwargs):
        product_id=self.kwargs["pk"]
        product=Product.objects.get(id=product_id)
        YOR_DOMAIN="http://127.0.0.1:8000"
        checkout_session = stripe.checkout.Session.create(
        line_items=[
                {
                    'price_data': {
                        'currency': 'usd',  # Ajusta a tu moneda
                        'product_data': {
                            'name': product.name,
                        },
                        'unit_amount': int(product.price * 100),  # Convertir a centavos
                    },
                    'quantity': 1,
                },
            ],
                mode='payment',
        success_url=YOUR_DOMAIN + '/success.html',
        cancel_url=YOUR_DOMAIN + '/cancel.html',
        )

def index(request):
    return render(request, 'index.html')
