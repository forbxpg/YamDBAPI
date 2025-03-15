from django.core.exceptions import ValidationError


def validator_forbidden_name(username):
    """Сверяет имя пользователя со списком запрещенных имен."""
    forrbidden_names = ('me',)
    if username.lower() in forrbidden_names:
        raise ValidationError(
            f'Имя пользователя {username} запрещено')
