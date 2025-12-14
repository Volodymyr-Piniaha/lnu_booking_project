# booking/models.py
from django.db import models
from django.contrib.auth.models import AbstractUser


# 1. Створення таблиці "User" (Користувачі)
# Ми розширюємо AbstractUser, щоб додати ваше поле Role
class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        ('user', 'User'),
        ('admin', 'Admin'),
    )
    # Замість FullName, Django використовує first_name та last_name (вони вже є)
    # Email та PasswordHash вже є в AbstractUser
    role = models.CharField(max_length=50, choices=ROLE_CHOICES, default='user')

    def __str__(self):
        return self.username


# 2. Створення таблиці "Hall" (Зали)
# (Замість HallID SERIAL, Django автоматично створить поле 'id')
class Hall(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True, null=True)
    capacity = models.IntegerField(blank=True, null=True)
    equipment_info = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name


# 3. Створення таблиці "TimeSlot" (Тайм-слоти)
class TimeSlot(models.Model):
    start_time = models.TimeField()
    end_time = models.TimeField()
    slot_name = models.CharField(max_length=100, blank=True, null=True)  # Наприклад, "Перша пара"

    def __str__(self):
        return f"{self.start_time.strftime('%H:%M')} - {self.end_time.strftime('%H:%M')}"


# 4. Створення таблиці "Reservation" (Бронювання)
class Reservation(models.Model):
    STATUS_CHOICES = (
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
        # Я додав 'pending' (очікує) згідно з вашими документами [cite: 98]
        ('pending', 'Pending'),
    )

    # Зв'язки (Foreign Keys)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    hall = models.ForeignKey(Hall, on_delete=models.CASCADE)
    timeslot = models.ForeignKey(TimeSlot, on_delete=models.CASCADE)

    reservation_date = models.DateField()
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='pending')

    class Meta:
        # Це реалізація вашого CONSTRAINT UQ_Reservation_Slot
        # Забороняє дублікати для (Hall, TimeSlot, ReservationDate)
        unique_together = ('hall', 'timeslot', 'reservation_date')

    def __str__(self):
        return f"{self.hall.name} - {self.timeslot} on {self.reservation_date} by {self.user.username}"