"""Валидаторы приложения users."""
from django.contrib.auth.validators import UnicodeUsernameValidator


class CustomUsernameValidator(UnicodeUsernameValidator):
    """Проверяет username пользователя."""

    regex = r'^[\w.@+-]+\Z'
    message = ('Enter a valid username. Required 150 characters or fewer. '
               'Letters, digits and @/./+/-/_ only.')
