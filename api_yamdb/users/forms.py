"""Формы приложения users."""
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserChangeForm, UserCreationForm

# User = get_user_model()
from .models import User


class CustomUserCreationForm(UserCreationForm):
    """Кастомная форма для создания пользователя.
    Наследуется от стандартной формы, изменяет модель пользователя на
    кастомную.
    """

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'email', 'role')


class CustomUserChangeForm(UserChangeForm):
    """Кастомная форма для изменения пользователя.
    Наследуется от стандартной формы, изменяет модель пользователя на
    кастомную.
    """

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'email', 'role')
