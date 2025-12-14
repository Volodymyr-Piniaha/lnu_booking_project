# booking/urls.py
from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views
from rest_framework.routers import DefaultRouter
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi



router = DefaultRouter()
router.register(r'halls', views.HallViewSet)
router.register(r'timeslots', views.TimeSlotViewSet)
router.register(r'reservations', views.ReservationViewSet, basename='api-reservation')

schema_view = get_schema_view(
   openapi.Info(
      title="LNU Booking API",
      default_version='v1',
      description="API для системи бронювання залів",
      contact=openapi.Contact(email="support@lnu.edu.ua"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    # 1. Головна сторінка (Каталог залів)
    path('', views.hall_list_view, name='hall_list'),

    # 2. Сторінка конкретного залу (його розклад)
    # <int:hall_id> - це динамічна частина, що прийматиме ID залу
    path('hall/<int:hall_id>/', views.hall_schedule_view, name='hall_schedule'),

    # 3. Сторінка "Мої бронювання"
    path('my-reservations/', views.my_reservations_view, name='my_reservations'),
    path('hall/<int:hall_id>/book/<int:slot_id>/<str:date>/', views.book_confirmation_view, name='book_confirmation'),
    path('signup/', views.signup_view, name='signup'),
# booking/urls.py
    path('cancel/<int:reservation_id>/', views.cancel_reservation_view, name='cancel_reservation'),
    # 2. Логін (стандартний view, але вказуємо наш шаблон)
    path('login/', views.CustomLoginView.as_view(), name='login'),

    # 3. Логаут (після виходу перекине на головну 'hall_list')
    # Починаючи з Django 5.0, LogoutView краще використовувати як POST запит,
    # але для простоти ми можемо використати вбудований метод.
    path('logout/', auth_views.LogoutView.as_view(next_page='hall_list'), name='logout'),


        path('api/', include(router.urls)),
]