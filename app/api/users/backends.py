from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from django.db.models import Q

class EmailOrUsernameModelBackend(ModelBackend):
    """
    Backend de autenticación personalizado que permite a los usuarios
    iniciar sesión utilizando tanto su nombre de usuario como su correo electrónico.
    """
    def authenticate(self, request, username=None, password=None, **kwargs):
        UserModel = get_user_model()
        try:
            # Buscar coincidencia insensible a mayúsculas en username o email
            user = UserModel.objects.get(
                Q(username__iexact=username) | Q(email__iexact=username)
            )
        except UserModel.DoesNotExist:
            return None
        
        # Verificar contraseña y si el usuario está activo
        if user.check_password(password) and self.user_can_authenticate(user):
            return user
        return None
