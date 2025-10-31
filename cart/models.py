from django.db import models
from uuid import uuid4
import secrets
from account.models import Buyer
from market.models import Product

class Cart(models.Model):
    cart_id = models.UUIDField(default=uuid4, primary_key=True)
    owner = models.OneToOneField(Buyer, related_name='cart_owner', on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    paid = models.BooleanField(default=False)

    def __str__(self):
        return str(self.cart_id)

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='cart')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='cart_product')
    added = models.DateTimeField(auto_now_add=True)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return str(self.cart.cart_id)

def get_order_id():
    id = secrets.token_hex(4)
    return id

class Order(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="cart_order")
    order_id = models.CharField(default=get_order_id, primary_key=True, unique=True, max_length=16)
    created = models.DateTimeField(auto_now_add=True)