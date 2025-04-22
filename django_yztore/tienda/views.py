from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.contrib import messages

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
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('tienda:inicio')
        else:
            messages.error(request, 'Usuario o contraseña incorrectos')
    return render(request, 'tienda/login.html')

def registro(request):
    if request.method == 'POST':
        # Aquí irá la lógica de registro
        pass
    return render(request, 'tienda/registro.html')

@login_required
def perfil(request):
    return render(request, 'tienda/perfil.html') 