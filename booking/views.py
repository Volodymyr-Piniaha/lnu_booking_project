# booking/views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Hall, TimeSlot, Reservation
from datetime import date, datetime
from django.contrib.auth import login
from .forms import CustomUserCreationForm
from django.views.decorators.http import require_POST
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from rest_framework import viewsets, permissions
from .serializers import HallSerializer, TimeSlotSerializer, ReservationSerializer


# 1. View для Головної сторінки (Список залів)
def hall_list_view(request):
    halls = Hall.objects.all()
    context = {
        'halls': halls
    }
    return render(request, 'booking/hall_list.html', context)


# 2. View для сторінки Залу (Розклад одного залу)
def hall_schedule_view(request, hall_id):
    hall = get_object_or_404(Hall, id=hall_id)
    timeslots = TimeSlot.objects.order_by('start_time')

    # --- НОВА ЛОГІКА ДАТИ ---
    # 1. Перевіряємо, чи передав користувач дату в URL (?date=2025-11-25)
    selected_date_str = request.GET.get('date')

    if selected_date_str:
        try:
            # Спробуємо перетворити рядок у дату
            selected_date = datetime.strptime(selected_date_str, '%Y-%m-%d').date()
        except ValueError:
            selected_date = date.today()
    else:
        # Якщо дати немає, беремо сьогодні
        selected_date = date.today()

    # Отримуємо заброньовані слоти саме для ОБРАНОЇ дати
    booked_slots_ids = Reservation.objects.filter(
        hall=hall,
        reservation_date=selected_date,
        status='confirmed'
    ).values_list('timeslot_id', flat=True)

    context = {
        'hall': hall,
        'timeslots': timeslots,
        'booked_slots_ids': set(booked_slots_ids),
        'selected_date': selected_date,  # Передаємо обрану дату в шаблон
    }
    return render(request, 'booking/hall_schedule.html', context)


# 3. View для "Моїх Бронювань" (Особистий кабінет)
@login_required  # Ця сторінка вимагатиме, щоб користувач увійшов
def my_reservations_view(request):
    # Беремо всі майбутні бронювання для поточного користувача
    reservations = Reservation.objects.filter(
        user=request.user,
        reservation_date__gte=date.today(),  # gte = "більше або дорівнює"
        status='confirmed'
    ).order_by('reservation_date', 'timeslot__start_time')  # Сортуємо

    context = {
        'reservations': reservations
    }
    return render(request, 'booking/my_reservations.html', context)


@login_required
def book_confirmation_view(request, hall_id, slot_id, date):  # Додали date_str
    hall = get_object_or_404(Hall, id=hall_id)
    slot = get_object_or_404(TimeSlot, id=slot_id)

    # Перетворюємо рядок дати з URL назад у об'єкт дати
    try:
        selected_date = datetime.strptime(date, '%Y-%m-%d').date()
    except ValueError:
        return redirect('hall_schedule', hall_id=hall.id)

    if request.method == 'POST':
        # Перевірка на подвійне бронювання перед збереженням
        if Reservation.objects.filter(hall=hall, timeslot=slot, reservation_date=selected_date,
                                      status='confirmed').exists():
            return render(request, 'booking/error.html', {'message': 'Цей слот вже зайнято!'})

        Reservation.objects.create(
            user=request.user,
            hall=hall,
            timeslot=slot,
            reservation_date=selected_date,  # Використовуємо дату з URL
            status='confirmed'
        )
        return redirect('my_reservations')

    context = {
        'hall': hall,
        'slot': slot,
        'date': selected_date
    }
    return render(request, 'booking/book_confirmation.html', context)


def signup_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Одразу логінимо користувача після реєстрації
            login(request, user)
            return redirect('hall_list')
    else:
        form = CustomUserCreationForm()

    return render(request, 'booking/signup.html', {'form': form})


@login_required
@require_POST
def cancel_reservation_view(request, reservation_id):
    # Шукаємо бронювання, яке належить САМЕ ЦЬОМУ користувачеві
    # Це захищає від видалення чужих бронювань
    reservation = get_object_or_404(Reservation, id=reservation_id, user=request.user)

    # Видаляємо запис (слот автоматично стає вільним, бо запис зникає)
    reservation.delete()

    # Повертаємо користувача назад на сторінку "Мої бронювання"
    return redirect('my_reservations')


class CustomLoginView(LoginView):
    template_name = 'booking/login.html'  # Вказуємо ваш шаблон

    def get_success_url(self):
        user = self.request.user

        # Перевіряємо, чи є користувач персоналом (is_staff) або суперюзером
        # Це найточніша перевірка для доступу в адмінку
        if user.is_staff or user.is_superuser:
            return '/admin/'

        # Якщо це звичайний користувач — повертаємо стандартний шлях
        # (який вказаний у settings.py як LOGIN_REDIRECT_URL)
        return reverse_lazy('hall_list')


class HallViewSet(viewsets.ModelViewSet):  # <--- Змінили на ModelViewSet (було ReadOnly...)
    """
    API для залів.
    - Читати список можуть всі.
    - Створювати/Редагувати/Видаляти - тільки Адміністратор.
    """
    queryset = Hall.objects.all()
    serializer_class = HallSerializer

    def get_permissions(self):
        # Якщо дія "небезпечна" (створення, зміна, видалення)
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [permissions.IsAdminUser()]  # Вимагаємо прав адмінистратора

        # Для всіх інших дій (перегляд списку) - доступ відкрито всім
        return [permissions.AllowAny()]


class TimeSlotViewSet(viewsets.ModelViewSet):  # <--- Змінили на ModelViewSet
    """
    API для тайм-слотів.
    - Читати список можуть всі.
    - Створювати/Редагувати/Видаляти - тільки Адміністратор.
    """
    queryset = TimeSlot.objects.order_by('start_time')
    serializer_class = TimeSlotSerializer

    def get_permissions(self):
        # Та ж логіка: змінює тільки адмін
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [permissions.IsAdminUser()]

        return [permissions.AllowAny()]

class ReservationViewSet(viewsets.ModelViewSet):
    """
    API для створення та управління бронюваннями.
    Користувач бачить і може змінювати ТІЛЬКИ свої бронювання.
    """
    serializer_class = ReservationSerializer
    permission_classes = [permissions.IsAuthenticated] # Тільки для зареєстрованих

    def get_queryset(self):
        # Повертаємо тільки бронювання поточного юзера (якщо це не адмін)
        user = self.request.user
        if user.is_staff:
            return Reservation.objects.all()
        return Reservation.objects.filter(user=user)

