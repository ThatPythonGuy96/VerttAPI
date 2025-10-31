from django.urls import path
from . import views
from rest_framework_simplejwt.views import TokenRefreshView

app_name = 'account'
urlpatterns = [
    path('login', views.LoginView.as_view(), name='login'),
    path('signup', views.SignupApi.as_view(), name='signup'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path('buyer', views.BuyerView.as_view(), name='buyer'),
    path('account', views.AccountView.as_view(), name='account'),
]