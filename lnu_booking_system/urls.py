# lnu_booking_system/urls.py
from django.contrib import admin
from django.urls import path, include
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

# Налаштування Swagger
schema_view = get_schema_view(
    openapi.Info(
        title="LNU Booking API",
        default_version='v1',
        description="API для бронювання спортивних залів",
        contact=openapi.Contact(email="admin@lnu.edu.ua"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),

    # Підключаємо всі URL з нашого додатку booking
    path('', include('booking.urls')),

    # --- SWAGGER (Документація) ---
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('accounts/', include('rest_framework.urls')),
]