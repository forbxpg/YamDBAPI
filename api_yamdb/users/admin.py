"""Регистрация модели пользователей в админке."""
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserCreationForm
from .models import User


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Email', {'fields': ('email',)}),
        ('Роль', {'fields': ('role',)})
    )

    list_display = (
        'username',
        'email',
        'role',
        'is_active',
        'date_joined',
        'last_login',
    )
    list_editable = (
        'role',
    )


CustomUserAdmin.fieldsets += (
    # Добавляем кортеж, где первый элемент — это название раздела в админке,
    # а второй элемент — словарь, где под ключом fields можно указать нужные поля.
    ('Биография', {'fields': ('bio',)}),
    ('Роль', {'fields': ('role',)}),
)

admin.site.register(User, CustomUserAdmin)
