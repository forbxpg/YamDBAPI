"""Регистрация модели пользователей в админке."""
from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserChangeForm, CustomUserCreationForm

User = get_user_model()


class CustomUserAdmin(UserAdmin):
    """Кастомный UserAdmin."""
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = User

    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Email', {'fields': ('email',)}),
        ('Роль', {'fields': ('role',)})
    )

    list_display = (
        'username',
        'email',
        'role',
        'is_superuser',
        'is_active',
        'date_joined',
        'last_login',
    )
    list_editable = (
        'role',
    )


CustomUserAdmin.fieldsets += (
    ('Биография', {'fields': ('bio',)}),
    ('Роль', {'fields': ('role',)}),
)

admin.site.register(User, CustomUserAdmin)
