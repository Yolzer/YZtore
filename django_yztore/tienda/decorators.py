from django.contrib.auth.decorators import user_passes_test
from django.core.exceptions import PermissionDenied
from functools import wraps
from django.shortcuts import redirect

def rol_requerido(roles_requeridos):
    """
    Decorador para verificar si el usuario tiene alguno de los roles requeridos
    """
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            try:
                rol_usuario = request.user.perfilusuario.rol
                if rol_usuario in roles_requeridos:
                    return view_func(request, *args, **kwargs)
                else:
                    raise PermissionDenied
            except:
                raise PermissionDenied
        return _wrapped_view
    return decorator

def admin_required(view_func):
    """
    Decorador para verificar si el usuario es administrador
    """
    return user_passes_test(
        lambda u: u.is_authenticated and u.perfilusuario.rol == 'admin',
        login_url='tienda:login'
    )(view_func)

def cliente_required(view_func):
    """
    Decorador para verificar si el usuario es cliente
    """
    return user_passes_test(
        lambda u: u.is_authenticated and u.perfilusuario.rol == 'cliente',
        login_url='tienda:login'
    )(view_func) 