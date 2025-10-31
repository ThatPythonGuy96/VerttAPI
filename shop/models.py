from django.db import models
from account.models import Seller

class Shop(models.Model):
    name = models.CharField(max_length=30)
    owner = models.ForeignKey(Seller, on_delete=models.CASCADE, related_name='shop_owner')
    is_active = models.BooleanField(default=True)
    verified = models.BooleanField(default=True)

    def __str__(self):
        return self.name
