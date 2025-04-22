from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import CustomUser, Role

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