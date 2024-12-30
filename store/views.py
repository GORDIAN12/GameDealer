import stripe
from django.views.generic import TemplateView  
from django.conf import settings
from django.shortcuts import render
from django.http import HttpResponse
from django.views import View

stripe.api_key=settings.STRIPE_SECRET_KEY

class ProductLandingPageView(TemplateView):
    template_name="landing.html"


class CreateCheckoutSessionView(View):
    def post(self, request, *args, **kwargs):
        YOR_DOMAIN="http://127.0.0.1:8000"
        checkout_session = stripe.checkout.Session.create(
        line_items=[
            {
                # Provide the exact Price ID (for example, pr_1234) of the product you want to sell
                'price': '{{PRICE_ID}}',
                'quantity': 1,
                },
            ],
        mode='payment',
        success_url=YOUR_DOMAIN + '/success.html',
        cancel_url=YOUR_DOMAIN + '/cancel.html',
        )

def index(request):
    return render(request, 'index.html')
