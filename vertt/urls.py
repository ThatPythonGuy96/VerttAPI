from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView
from django.conf import settings
from django.conf.urls.static import static
# from rest_framework.schemas import get_schema_view
# from rest_framework.documentation import include_docs_urls

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/', include('account.urls', namespace='account')),
    path('api/shop/', include('shop.urls', namespace='shop')),
    path('api/cart/', include('cart.urls', namespace='cart')),
    path('api/market/', include('market.urls', namespace='market')),

    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),

    # YOUR PATTERNS
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    # Optional UI:
    path('', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),

    # path('project/docs/', include_docs_urls(title="VerttAPI")),
    # path('project/schema', get_schema_view(
    #         title="VerttAPI",
    #         description="An online shoop",
    #         version="1.0.0"
    #     ), name='openapi-schema')
]

urlpatterns += static(settings.STATIC_URL, document_root = settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)