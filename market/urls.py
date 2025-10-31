from django.urls import path
from . import views

app_name = 'market'
urlpatterns = [
    path('products', views.ProductsView.as_view(), name='products'),
    path('products/<str:order>', views.ProductsOrderByView.as_view(), name='products_order_by'),
    path('product/<int:id>', views.ProductView.as_view(), name='product'),
    path('product/create', views.CreateProductView.as_view(), name='create_product'),
    path('categories', views.CategoriesView.as_view(), name='categories'),
    path('category/<int:id>', views.CategoryView.as_view(), name='category'),
    path('subcategories', views.SubcategoriesView.as_view(), name='subcategories'),
    path('subcategory/<int:id>', views.SubcategoryView.as_view(), name='subcategory'),
]