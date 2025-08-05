from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model

User = get_user_model()

class IDNumberAuthBackend(ModelBackend):
    """
    Custom authentication backend that allows users to log in using their
    ID number (stored in the 'id_number' field) instead of username.
    """

    def authenticate(self, request, id_number=None, password=None, **kwargs):
        if id_number is None:
            id_number = kwargs.get('username')  # fallback if called with username param
        try:
            user = User.objects.get(id_number=id_number)
        except User.DoesNotExist:
            return None

        if user.check_password(password) and self.user_can_authenticate(user):
            return user
        return None
