from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model

User = get_user_model()

class IDNumberBackend(ModelBackend):
    """
    Custom authentication backend that allows users to log in using their
    ID number (stored in the 'id_number' field) instead of username.
    """

    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = User.objects.get(id_number=username)
        except User.DoesNotExist:
            return None

        if user.check_password(password) and self.user_can_authenticate(user):
            return user
        return None

