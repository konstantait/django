from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from phonenumber_field.validators import validate_international_phonenumber

UserModel = get_user_model()


class EmailBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        if username is None:
            username = kwargs.get(UserModel.USERNAME_FIELD)
        if username is None or password is None:
            return None
        try:
            validate_email(username)
        except ValidationError:
            return None
        try:
            user = UserModel.objects.get(email=username)
        except UserModel.DoesNotExist:
            UserModel().set_password(password)
        else:
            if user.check_password(password) and self.user_can_authenticate(user): # noqa
                return user

    def user_can_authenticate(self, user):
        return getattr(user, "is_active", True)


class PhoneBackend(ModelBackend):
        def authenticate(self, request, username=None, password=None, **kwargs): # noqa
            if username is None:
                username = kwargs.get(UserModel.USERNAME_FIELD)
            if username is None or password is None:
                return None
            try:
                validate_international_phonenumber(username)
            except ValidationError:
                return None
            try:
                user = UserModel.objects.get(phone=username)
            except UserModel.DoesNotExist:
                UserModel().set_password(password)
            else:
                if user.check_password(password) and self.user_can_authenticate(user): # noqa
                    return user

        def user_can_authenticate(self, user):
            valid = getattr(user, "is_active", True)
            valid &= getattr(user, "is_phone_valid", False)
            return valid
