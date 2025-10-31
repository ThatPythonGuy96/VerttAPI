import random
import faker.providers
from faker import Faker
from django.core.management.base import BaseCommand
from account.models import Account, Buyer, Seller
from market.models import Category, SubCategory, Product, ProductImage
from shop.models import Shop

CATEGORIES = [
    "Phone & Tablets",
    "Electronics",
    "Home & Office",
    "Men's Fashion",
    "Women's Fashion",
    "Gaming",
    "Sporting",
    "Computing",
    "Health & Beauty"
]

SUBCATEGORIES = [
    "iPhone",
    "Andriod",
    "Tablet",
    "Accessories",
    "Sound Bar",
    "Smart Tv",
    "Cleansers",
    "Face Care",
    "Home Decor",
    "Office Accessories",
    "Office Supply",
    "Laptops",
    "Printers",
    "Gaming Laptops",
    "Shoes",
    "Clothing",
    "Watches",
    "Jewelry",
    "Boots",
    "Men Underwears",
    "PS4",
    "PSP",
    "Gaming Chair",
    "PS5",
    "Workout",
    "Equipment",
    "Fitness Tech",
]

PRODUCTS = [
    "Itel P500 3GB 32BG",
    "LOWA Men\’s Renegade GTX Mi",
    "Samsung s24 Ultra",
    "Samsung Galaxy A05 6.7\" 4GB RAM/64GB ROM Android 13",
    "itel VistaTab 10 Mini 8\" 3GB RAM/64GB ROM Android 14 - Grey",
    "Apple IPhone 11 Pro Max (4GBRAM, 256GB ROM) 4G Midnight Green",
    "LifeTime Quality Office Chair",
    "Chelsea Boot",
]

class Provider(faker.providers.BaseProvider):
    def category(self):
        return self.random_element(CATEGORIES)
    
    def subcategory(self):
        return self.random_element(SUBCATEGORIES)
    
    def product(self):
        return self.random_element(PRODUCTS)
    
class Command(BaseCommand):
    help = "Generate fake data"

    def handle(self, *args, **kwargs):
        fake = Faker()
        fake.add_provider(Provider)

        for _ in range(9):
            d = fake.unique.category()
            Category.objects.create(category=d)
        
        for _ in range(27):
            su = fake.unique.subcategory()
            cat = list(Category.objects.all())
            SubCategory.objects.create(subcategory=su, category=random.choice(cat))
        
        for _ in range(8):
            name_ = fake.unique.product()
            cat = list(Category.objects.all())
            sub = list(SubCategory.objects.all())
            shops = list(Shop.objects.all())

            Product.objects.create(
                name = name_,
                description = fake.text(max_nb_chars=50),
                category = random.choice(cat),
                subcategory = random.choice(sub),
                price = (round(random.uniform(3000.99, 500000.00), 2)),
                discount_price = (round(random.uniform(2000.99, 9000.00), 2)),
                quantity = random.randint(1, 30),
                shop = random.choice(shops)
            )

        self.stdout.write(self.style.SUCCESS("Fake data generated successfully!"))
