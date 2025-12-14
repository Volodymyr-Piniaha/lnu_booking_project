# booking/serializers.py
from rest_framework import serializers
from .models import Hall, TimeSlot, Reservation
import datetime


# 1. Серіалізатор для Залів
class HallSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hall
        fields = '__all__'  # Віддаємо всі поля (id, name, description...)


# 2. Серіалізатор для Тайм-слотів
class TimeSlotSerializer(serializers.ModelSerializer):
    class Meta:
        model = TimeSlot
        fields = '__all__'


# 3. Серіалізатор для Бронювань
class ReservationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reservation
        fields = '__all__'
        # Робимо поля user та status доступними тільки для читання,
        # щоб користувач не міг бронювати від чужого імені або зразу ставити статус
        read_only_fields = ('user', 'status')

    def create(self, validated_data):
        # Автоматично підставляємо поточного користувача
        validated_data['user'] = self.context['request'].user
        validated_data['status'] = 'confirmed'
        return super().create(validated_data)

    # --- ОСЬ ТУТ ЛОГІКА ПЕРЕВІРКИ (UQ_Reservation_Slot) ---
    def validate(self, data):
        # Отримуємо дані, які надіслав юзер
        hall = data.get('hall')
        timeslot = data.get('timeslot')
        reservation_date = data.get('reservation_date')

        # Перевірка 1: Чи не намагаються забронювати минуле?
        if reservation_date < datetime.date.today():
             raise serializers.ValidationError("Не можна бронювати зали на минулі дати!")

        # Перевірка 2 (UQ_Reservation_Slot): Чи зайнятий цей слот?
        # Шукаємо в базі запис з таким же залом, часом, датою І статусом 'confirmed'
        duplicate_exists = Reservation.objects.filter(
            hall=hall,
            timeslot=timeslot,
            reservation_date=reservation_date,
            status='confirmed'
        ).exists()

        if duplicate_exists:
            # Якщо знайшли дублікат - викидаємо помилку валідації
            # Це поверне JSON: { "non_field_errors": ["На цей час зал вже заброньовано."] }
            raise serializers.ValidationError("На жаль, на цей час зал вже заброньовано.")

        return data