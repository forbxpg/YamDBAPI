from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail


def send_code_to_email(user):
    """Отправка кода подтверждения на email."""
    confirmation_code = default_token_generator.make_token(user)
    send_mail(
        subject='YamDB: Mail confirmation.',
        message=(
            f'Уважаемый, {user.username}.\n'
            'Вы получили это письмо, потому что вашу почту указали '
            'при регистрации на портале YamDB.\n'
            'Ваш код для получения JWT токена:\n'
            f'{confirmation_code}'
        ),
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[user.email],
        fail_silently=False,
    )
