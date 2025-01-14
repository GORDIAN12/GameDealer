from django.db import models
from django.contrib.auth.models import User

class UserPayment(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    stripe_customer_id=models.CharField(max_length=255)
    stripe_checkout_id=models.CharField(max_length=255)
    product_name=models.CharField(max_length=255)
    quantity=models.IntegerField(default=1)
    price=models.DecimalField(max_digits=10, decimal_places=2)
    currency=models.CharField(max_length=3)
    has_paid=models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.user.username} - {self.product_name} - Paid: {self.has_paid}" 

class Product(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField()
    imagen = models.ImageField(upload_to='static/', null=True, blank=True)

    def __str__(self):
        return self.nombre


