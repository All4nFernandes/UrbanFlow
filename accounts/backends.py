import re

from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend


class CPFOrUsernameBackend(ModelBackend):
    """Authenticate with the existing username or the stored CPF."""

    def authenticate(self, request, username=None, password=None, **kwargs):
        UserModel = get_user_model()
        if username is None:
            username = kwargs.get(UserModel.USERNAME_FIELD)
        if not username or not password:
            return None

        try:
            user = UserModel._default_manager.get_by_natural_key(username)
        except UserModel.DoesNotExist:
            cpf = re.sub(r"\D", "", username)
            if len(cpf) != 11:
                return None
            try:
                user = UserModel._default_manager.get(cpf=cpf)
            except UserModel.DoesNotExist:
                return None

        if user.check_password(password) and self.user_can_authenticate(user):
            return user
        return None
