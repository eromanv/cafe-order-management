from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from orders.api_views import OrderViewSet
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions

schema_view = get_schema_view(
    openapi.Info(
        title="Cafe Order Management API",
        default_version='v1',
        description="API documentation for the Cafe Order Management system",
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

router = DefaultRouter()
router.register(r"orders", OrderViewSet)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("orders/", include("orders.urls")),
    path("api/", include(router.urls)),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path("api-auth/", include("rest_framework.urls")),
]
