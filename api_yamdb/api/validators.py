import re

from django.core.exceptions import ValidationError


def username_validator(username):
    if username.lower() == 'me':
        raise ValidationError(
            'Имя пользователя "me" запрещено')
    elif re.match(r'^[\w.@+-]+\Z', username) is None:
        raise ValidationError(
            'Имя пользователя содержит недопустимые символы.'
        )
    return username
