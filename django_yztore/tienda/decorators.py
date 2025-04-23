from django.contrib.auth.decorators import user_passes_test
from django.core.exceptions import PermissionDenied
from functools import wraps
from django.shortcuts import redirect
from django.core.cache import cache
from django.http import HttpResponseForbidden
from django.conf import settings
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.decorators import login_required

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

def rate_limit_login(attempts=3, timeout=300):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if request.method == 'POST':
                ip = request.META.get('REMOTE_ADDR')
                cache_key = f'login_attempts_{ip}'
                attempts_count = cache.get(cache_key, 0)
                
                if attempts_count >= attempts:
                    return HttpResponseForbidden('Demasiados intentos de inicio de sesión. Por favor, intente más tarde.')
                
                cache.set(cache_key, attempts_count + 1, timeout)
                
                response = view_func(request, *args, **kwargs)
                
                if hasattr(response, 'status_code') and response.status_code == 200:
                    cache.delete(cache_key)
                
                return response
            
            return view_func(request, *args, **kwargs)
        return _wrapped_view
    return decorator

def sanitize_input(func):
    @wraps(func)
    def wrapper(request, *args, **kwargs):
        if request.method == 'POST':
            # Sanitizar datos POST
            for key, value in request.POST.items():
                if isinstance(value, str):
                    request.POST[key] = value.strip()
        return func(request, *args, **kwargs)
    return wrapper 