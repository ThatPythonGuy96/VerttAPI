from django.contrib import admin
from . import models

@admin.register(models.Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = ('id', 'email', 'is_admin', 'is_verified')

@admin.register(models.Buyer)
class BuyerAdmin(admin.ModelAdmin):
    list_display = ('account',)

@admin.register(models.Seller)
class SellerAdmin(admin.ModelAdmin):
    list_display = ('account',)

@admin.register(models.ShippingInfo)
class ShippingInfoAdmin(admin.ModelAdmin):
    list_display = ('buyer',)