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

def inicio(request):
    return render(request, 'tienda/inicio.html')

def juegos(request):
    return render(request, 'tienda/juegos.html')

def ofertas(request):
    return render(request, 'tienda/ofertas.html')

@login_required
def carrito(request):
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

def registro_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        
        if password1 != password2:
            messages.error(request, 'Las contraseñas no coinciden')
            return render(request, 'tienda/registro.html')
        
        if CustomUser.objects.filter(email=email).exists():
            messages.error(request, 'El email ya está registrado')
            return render(request, 'tienda/registro.html')
            
        if CustomUser.objects.filter(username=username).exists():
            messages.error(request, 'El nombre de usuario ya está en uso')
            return render(request, 'tienda/registro.html')
            
        # Crear usuario
        cliente_role = Role.objects.get(nombre='cliente')
        user = CustomUser.objects.create_user(
            username=username,
            email=email,
            password=password1,
            rol=cliente_role
        )
        login(request, user)
        return redirect('tienda:inicio')
        
    return render(request, 'tienda/registro.html')

@login_required
def logout_view(request):
    logout(request)
    return redirect('tienda:inicio')

@login_required
def perfil(request):
    return render(request, 'tienda/perfil.html')

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