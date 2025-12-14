# booking/admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Hall, TimeSlot, Reservation

# Налаштовуємо адмінку для CustomUser, щоб вона показувала наше поле 'role'
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    # Додаємо 'role' до полів, які видно при редагуванні
    fieldsets = UserAdmin.fieldsets + (
        ('Custom Fields', {'fields': ('role',)}),
    )
    # Додаємо 'role' до полів, які видно при створенні
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Custom Fields', {'fields': ('role',)}),
    )

# Реєструємо ваші моделі в адмін-панелі
admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Hall)
admin.site.register(TimeSlot)
admin.site.register(Reservation)