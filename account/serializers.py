from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password
from . import models
from shop.serializers import ShopSerializer

class LoginTokenSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, account):
        token = super().get_token(account)
        token['email'] = account.email
        return token

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')
        try:
            account = models.Account.objects.get(email=email)
            if not account.is_active:
                raise serializers.ValidationError("Your Account is Not active. Activate Your Account to login.")
            if not account.check_password(password):
                raise serializers.ValidationError({"error": "Incorrect Password."})
        except models.Account.DoesNotExist:
            raise serializers.ValidationError("No Account Found with given credentials")
        data = super().validate(attrs)
        data['email'] = account.email
        return data
    
class SignupSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True, validators=[UniqueValidator(queryset=models.Account.objects.all())])
    password1 = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = models.Account
        fields = ('email', 'password1', 'password2')
        extra_kwargs = {"password1": {"write_only": True}, "password2": {"write_only": True}}

    def validate(self, attrs):
        if attrs['password1'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields don't match."})
        return attrs
    
    def create(self, validated_data):
        account = models.Account.objects.create(
            email=validated_data['email'],
        )
        account.set_password(validated_data['password1'])
        account.save()
        return account
    
class ShippingSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.ShippingInfo
        fields = '__all__'

class BuyerSerializer(serializers.ModelSerializer):
    # account = AccountSerializer()
    shipping_details = serializers.SerializerMethodField()

    def get_shipping_details(self, obj):
        shipping = models.ShippingInfo.objects.get(buyer=obj)
        return ShippingSerializer(shipping).data 
           
    class Meta:
        model = models.Buyer
        fields = ['account', 'first_name', 'last_name', 'shipping_details']

class SellerSerializer(serializers.ModelSerializer):
    # account = AccountSerializer()
    shop = ShopSerializer()
    
    class Meta:
        model = models.Seller
        fields = ['account', 'shop']


class AccountSerializer(serializers.ModelSerializer):
    buyer = BuyerSerializer()
    seller = SellerSerializer()

    class Meta:
        model = models.Account
        fields = ['id', 'email', 'is_buyer', 'is_seller', 'buyer', 'seller']