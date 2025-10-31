from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from uuid import uuid4

class AccountManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_admin', True)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_verified', True)
        return self.create_user(email, password, **extra_fields)

class Account(AbstractBaseUser, PermissionsMixin):
    id = models.UUIDField(primary_key=True, max_length=10, default=uuid4, editable=False)
    email = models.EmailField(unique=True)
    date_joined = models.DateTimeField(auto_now_add=True)    
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    
    objects = AccountManager()

    class Meta:
        ordering = ['-date_joined']
        verbose_name_plural = "accounts"

    def __str__(self):
        return self.email

    @property
    def is_buyer(self):
        return hasattr(self, 'buyer')

    @property
    def is_seller(self):
        return hasattr(self, 'seller')

#==========================BUYER======================================
class Buyer(models.Model):
    account = models.OneToOneField(Account, on_delete=models.CASCADE, related_name='buyer')
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    date_of_birth = models.DateField()

    def __str__(self):
        return self.account.email

class ShippingInfo(models.Model):
    buyer = models.OneToOneField(Buyer, on_delete=models.CASCADE, related_name='buyer_shipping_info')
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    address1 = models.CharField(max_length=30)
    address2 = models.CharField(max_length=30, null=True, blank=True)
    phone1 = models.PositiveBigIntegerField()
    phone2 = models.PositiveBigIntegerField(null=True, blank=True)
    city = models.CharField(max_length=12)
    state = models.CharField(max_length=12)
    
    def ___str___(self):
        return f"{self.buyer.email} shopping details"
    
#==========================SELLER======================================
class Seller(models.Model):
    account = models.OneToOneField(Account, on_delete=models.CASCADE, related_name='seller')

    def __str__(self):
        return self.account.email