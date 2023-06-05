from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_decode
from django.utils.http import urlsafe_base64_encode
from django.core.exceptions import ValidationError
from django.contrib.auth.tokens import default_token_generator

from profiles.models import User


def get_uidb64_from_pk(pk: User.pk) -> str:
    return urlsafe_base64_encode(force_bytes(pk))


def get_user_token(user: User) -> str:
    return default_token_generator.make_token(user)


def get_user_by_uidb64(uidb64: str) -> User:
    try:
        user = User.objects.get(pk=urlsafe_base64_decode(uidb64).decode())
    except (
            TypeError,
            ValueError,
            OverflowError,
            User.DoesNotExist,
            ValidationError,
    ):
        user = None
    return user


def user_activated_by_token(uidb64: str, token: str) -> bool:
    user = get_user_by_uidb64(uidb64)
    if user and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
    return user
