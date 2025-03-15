from datetime import datetime as dt

from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


def validate_year(value: int) -> None:
    now = dt.now().year
    if value > now:
        raise ValidationError(
            _('Год произведения не может быть больше текущего!')
        )
