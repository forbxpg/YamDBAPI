"""Формы приложения users."""
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserChangeForm, UserCreationForm

from api_yamdb.settings import USERS_ROLE

User = get_user_model()


class CustomUserCreationForm(UserCreationForm):
    """Кастомная форма для создания пользователя.
    Наследуется от стандартной формы, изменяет модель пользователя на
    кастомную.
    """

    class Meta(UserCreationForm.Meta):
        """Meta."""
        model = User
        fields = ('username', 'email', 'role')

    def save(self, commit=True):
        """Переопределяем метод save для админ панели."""
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if (user.role == USERS_ROLE['admin']):
            user.is_staff = True
        else:
            user.is_staff = False
        if commit:
            user.save()
        return user


class CustomUserChangeForm(UserChangeForm):
    """Кастомная форма для изменения пользователя.
    Наследуется от стандартной формы, изменяет модель пользователя на
    кастомную.
    """

    class Meta(UserCreationForm.Meta):
        """Meta."""
        model = User
        fields = ('username', 'email', 'role')
