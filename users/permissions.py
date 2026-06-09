from django.utils import timezone
from django.db.models import Q
from rest_framework import permissions
from .models import UserProfileAssignment

def get_user_active_permissions(user):
    """
    Retorna un diccionario con los códigos de permisos activos del usuario
    y su alcance correspondiente (el alcance 'todos' prevalece sobre 'propios').
    """
    if not user.is_authenticated:
        return {}

    if user.is_superuser:
        # El superusuario tiene acceso a todo con el máximo alcance
        return {"all": "todos"}

    now = timezone.now()
    
    # Obtener todas las asignaciones de perfil activas y que no hayan expirado
    active_assignments = UserProfileAssignment.objects.filter(
        user=user,
        is_active=True
    ).filter(
        Q(expires_at__isnull=True) | Q(expires_at__gt=now)
    ).select_related('profile')

    user_permissions = {}

    for assignment in active_assignments:
        # Consultar las asociaciones perfil-permiso
        profile_perms = assignment.profile.profilepermission_set.select_related('permission')
        for pp in profile_perms:
            code = pp.permission.code
            scope = pp.scope # 'propios' o 'todos'

            if code not in user_permissions:
                user_permissions[code] = scope
            else:
                # Si ya existía, prevalece el mayor alcance ('todos' > 'propios')
                if scope == 'todos':
                    user_permissions[code] = 'todos'

    return user_permissions


def has_custom_permission(user, permission_code, required_scope='propios'):
    """
    Verifica si el usuario tiene un permiso específico con el alcance requerido.
    """
    perms = get_user_active_permissions(user)
    
    # Superusuario pasa siempre
    if "all" in perms:
        return True

    if permission_code not in perms:
        return False

    user_scope = perms[permission_code]
    
    # Si se requiere 'todos' pero el usuario solo tiene alcance 'propios', denegamos el acceso
    if required_scope == 'todos' and user_scope == 'propios':
        return False

    return True


class HasDynamicPermission(permissions.BasePermission):
    """
    Clase de permiso personalizada para Django REST Framework.
    Permite asegurar vistas basadas en códigos de permisos dinámicos.
    
    Uso en Vista:
        permission_classes = [HasDynamicPermission]
        required_permission = 'banners:crear'
        required_scope = 'todos' # opcional, por defecto 'propios'
    """
    
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False

        # Si la vista no define un permiso requerido, se asume que basta con estar autenticado
        required_permission = getattr(view, 'required_permission', None)
        if not required_permission:
            return True

        required_scope = getattr(view, 'required_scope', 'propios')
        return has_custom_permission(request.user, required_permission, required_scope)
