from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.utils.crypto import get_random_string
from django.utils import timezone
from datetime import timedelta
from .models import CustomUser, Role, TokenRecuperacion
from .forms import RegistroForm
from .models import PerfilUsuario
from .decorators import admin_required

def inicio(request):
    return render(request, 'tienda/inicio.html')

def juegos_view(request):
    return render(request, 'tienda/juegos.html')

def ofertas_view(request):
    return render(request, 'tienda/ofertas.html')

@login_required
def carrito_view(request):
    return render(request, 'tienda/carrito.html')

def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('tienda:inicio')
        else:
            messages.error(request, 'Email o contraseña incorrectos')
    return render(request, 'tienda/login.html')

def registro(request):
    if request.method == 'POST':
        form = RegistroForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, '¡Registro exitoso!')
            return redirect('tienda:inicio')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
    else:
        form = RegistroForm()
    return render(request, 'tienda/registro.html', {'form': form})

@login_required
def logout_view(request):
    logout(request)
    return redirect('tienda:inicio')

@login_required
def perfil(request):
    perfil = request.user.perfilusuario
    if request.method == 'POST':
        form = PerfilForm(request.POST, instance=perfil)
        if form.is_valid():
            form.save()
            messages.success(request, 'Perfil actualizado correctamente')
            return redirect('tienda:perfil')
    else:
        form = PerfilForm(instance=perfil)
    return render(request, 'tienda/perfil.html', {'form': form})

def recuperar_password_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        try:
            user = CustomUser.objects.get(email=email)
            # Generar token
            token = get_random_string(length=32)
            # Crear o actualizar token de recuperación
            token_recuperacion, created = TokenRecuperacion.objects.update_or_create(
                user=user,
                defaults={
                    'token': token,
                    'fecha_expiracion': timezone.now() + timedelta(hours=24)
                }
            )
            
            # Enviar correo
            reset_url = request.build_absolute_uri(f'/restablecer-password/{token}/')
            send_mail(
                'Recuperación de Contraseña - YZtore',
                f'Para restablecer tu contraseña, haz clic en el siguiente enlace: {reset_url}',
                settings.EMAIL_HOST_USER,
                [email],
                fail_silently=False,
            )
            
            messages.success(request, 'Se ha enviado un correo con las instrucciones para restablecer tu contraseña')
            return redirect('tienda:login')
        except CustomUser.DoesNotExist:
            messages.error(request, 'No existe una cuenta con ese correo electrónico')
    
    return render(request, 'tienda/recuperar_password.html')

def restablecer_password_view(request, token):
    try:
        token_recuperacion = TokenRecuperacion.objects.get(
            token=token,
            fecha_expiracion__gt=timezone.now()
        )
        
        if request.method == 'POST':
            password1 = request.POST.get('password1')
            password2 = request.POST.get('password2')
            
            if password1 != password2:
                messages.error(request, 'Las contraseñas no coinciden')
                return render(request, 'tienda/restablecer_password.html')
            
            # Cambiar contraseña
            user = token_recuperacion.user
            user.set_password(password1)
            user.save()
            
            # Eliminar token
            token_recuperacion.delete()
            
            messages.success(request, 'Tu contraseña ha sido restablecida correctamente')
            return redirect('tienda:login')
            
        return render(request, 'tienda/restablecer_password.html')
    except TokenRecuperacion.DoesNotExist:
        messages.error(request, 'El enlace de recuperación no es válido o ha expirado')
        return redirect('tienda:recuperar_password')

@admin_required
def gestion_usuarios(request):
    usuarios = CustomUser.objects.all()
    return render(request, 'tienda/admin/gestion_usuarios.html', {'usuarios': usuarios})

@admin_required
def cambiar_rol_usuario(request, user_id):
    if request.method == 'POST':
        try:
            usuario = CustomUser.objects.get(id=user_id)
            nuevo_rol = request.POST.get('rol')
            if nuevo_rol in ['cliente', 'admin']:
                perfil = usuario.perfilusuario
                perfil.rol = nuevo_rol
                perfil.save()
                messages.success(request, f'Rol de {usuario.username} actualizado correctamente')
            else:
                messages.error(request, 'Rol no válido')
        except CustomUser.DoesNotExist:
            messages.error(request, 'Usuario no encontrado')
    return redirect('tienda:gestion_usuarios') 