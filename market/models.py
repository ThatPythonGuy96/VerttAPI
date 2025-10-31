from django.db import models
import random, os
from uuid import uuid4
from shop.models import Shop
from account.models import Buyer
from django.utils.safestring import mark_safe
from django.core.validators import FileExtensionValidator

class Category(models.Model):
    category = models.CharField(max_length=20)
    image = models.ImageField(upload_to='category/')

    def __str__(self):
        return self.category

    def image_tag(self):
        return mark_safe('<img src="/../../media/%s" width="100" height="100" />' % (self.image))

class SubCategory(models.Model):
    subcategory = models.CharField(max_length=20)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="subcategory")

    def __str__(self):
        return f"{self.subcategory} - {self.category}"
    
def product_id():
    return random.randrange(000000, 999999)

class Product(models.Model):
    id = models.IntegerField(primary_key=True, default=product_id)
    name = models.CharField(max_length=100)
    description = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='product_category')
    subcategory = models.ForeignKey(SubCategory, on_delete=models.CASCADE, related_name='product_subcategory')
    price = models.PositiveBigIntegerField()
    discount_price = models.PositiveBigIntegerField(null=True, blank=True)
    quantity = models.IntegerField()
    rating = models.IntegerField(default=0)
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE, related_name='product_shop')
    on_sale = models.BooleanField(default=True)
    added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

def get_product_images(instance, filename):
    upload_to = '{}/{}/{}'.format('shop', instance.product.shop, 'product')
    ext = filename.split('.')[-1]
    name = instance.product.name[:10]
    filename = '{}.{}'.format(name, ext)
    return os.path.join(upload_to, filename)

class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product_image')
    image = models.ImageField(upload_to=get_product_images, validators=[FileExtensionValidator(['png', 'jpg', 'jpeg'])])

    def image_tag(self):
        return mark_safe('<img src="/../../media/%s" width="100" height="100" />' % (self.image))

class WatchList(models.Model):
    watchlist_id = models.UUIDField(default=uuid4, primary_key=True)
    account = models.OneToOneField(Buyer, on_delete=models.CASCADE, related_name='watchlist_owner')

class WatchListProduct(models.Model):
    watchlist = models.ForeignKey(WatchList, on_delete=models.CASCADE, related_name='watchlist')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='watchlist_product')
    added = models.DateTimeField(auto_now_add=True)