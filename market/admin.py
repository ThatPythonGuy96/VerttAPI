from django.contrib import admin
from . import models

class ProductImageInline(admin.TabularInline):
    model = models.ProductImage
    extra = 3
    fields = ['image']

@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'price', 'discount_price')
    list_filter = ('shop',)
    inlines = [ProductImageInline]

@admin.register(models.Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('category', 'image_tag')

@admin.register(models.SubCategory)
class SubCategoryAdmin(admin.ModelAdmin):
    list_display = ('subcategory', 'category')