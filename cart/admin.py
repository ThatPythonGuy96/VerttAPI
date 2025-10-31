from django.contrib import admin
from . import models

class CartItemInline(admin.TabularInline):
    model = models.CartItem
    extra = 1

@admin.register(models.Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('cart_id', 'owner', 'created', 'modified')
    inlines = [CartItemInline]

@admin.register(models.CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'cart', 'product', 'added', 'quantity')