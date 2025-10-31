from django.urls import path
from . import views

app_name = 'cart'
urlpatterns = [
    path('', views.CartView.as_view(), name='cart'),
    path('add/', views.AddCartItem.as_view(), name='add_cartitem'),
    path('update/', views.UpdateCart.as_view(), name='update_cart'),
    path('<int:cartitem_id>/delete', views.DeleteCartItem.as_view(), name='delete_cartitem'),
    path('product_in_cart/<int:product_id>', views.ProductInCart.as_view(), name="product_in_cart"),
]