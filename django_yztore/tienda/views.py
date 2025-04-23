from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.utils.crypto import get_random_string
from django.utils import timezone
from datetime import timedelta
from django.views.decorators.csrf import csrf_protect
from django.core.exceptions import ValidationError
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.decorators.csrf import csrf_protect
from django.utils.decorators import method_decorator
from .models import CustomUser, Role, TokenRecuperacion, Juego, Carrito, CarritoItem, Producto, PerfilUsuario
from .forms import RegistroForm, PerfilForm
from .decorators import admin_required, rate_limit_login, sanitize_input
from .services import ProductoService, CarritoService, UsuarioService

class InicioView(ListView):
    template_name = 'tienda/inicio.html'
    context_object_name = 'productos'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['productos_destacados'] = ProductoService.obtener_productos_destacados()
        context['productos_ofertas'] = ProductoService.obtener_productos_ofertas()
        return context

    def get_queryset(self):
        return Producto.objects.none()

class ProductoListView(ListView):
    model = Producto
    template_name = 'tienda/productos.html'
    context_object_name = 'productos'
    paginate_by = 12

    def get_queryset(self):
        categoria = self.request.GET.get('categoria')
        orden = self.request.GET.get('orden', 'recientes')
        return ProductoService.filtrar_productos(categoria, orden)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categoria'] = self.request.GET.get('categoria')
        context['orden_actual'] = self.request.GET.get('orden', 'recientes')
        return context

class ProductoDetailView(DetailView):
    model = Producto
    template_name = 'tienda/detalle_producto.html'
    context_object_name = 'producto'

class PerfilUpdateView(LoginRequiredMixin, UpdateView):
    model = PerfilUsuario
    form_class = PerfilForm
    template_name = 'tienda/perfil.html'
    success_url = reverse_lazy('tienda:perfil')

    def get_object(self):
        return self.request.user.perfilusuario

    @method_decorator(csrf_protect)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

@csrf_protect
@rate_limit_login(attempts=5, timeout=900)
@sanitize_input
def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email', '').strip()
        password = request.POST.get('password', '').strip()
        
        if not email or not password:
            messages.error(request, 'Por favor, complete todos los campos')
            return render(request, 'tienda/login.html')
            
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('tienda:inicio')
        else:
            messages.error(request, 'Email o contraseña incorrectos')
    return render(request, 'tienda/login.html')

@csrf_protect
@sanitize_input
def registro(request):
    if request.method == 'POST':
        form = RegistroForm(request.POST)
        if form.is_valid():
            try:
                user = form.save()
                login(request, user)
                messages.success(request, '¡Registro exitoso!')
                return redirect('tienda:inicio')
            except ValidationError as e:
                messages.error(request, str(e))
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
    else:
        form = RegistroForm()
    return render(request, 'tienda/registro.html', {'form': form})

@login_required
def carrito_view(request):
    carrito = CarritoService.obtener_carrito_usuario(request.user)
    total = CarritoService.calcular_total_carrito(carrito)
    return render(request, 'tienda/carrito.html', {
        'carrito': carrito,
        'total': total
    })

@login_required
def logout_view(request):
    logout(request)
    return redirect('tienda:inicio')

@csrf_protect
@login_required
def perfil(request):
    perfil = request.user.perfilusuario
    if request.method == 'POST':
        form = PerfilForm(request.POST, instance=perfil)
        if form.is_valid():
            try:
                form.save()
                messages.success(request, 'Perfil actualizado correctamente')
                return redirect('tienda:perfil')
            except ValidationError as e:
                messages.error(request, str(e))
    else:
        form = PerfilForm(instance=perfil)
    return render(request, 'tienda/perfil.html', {'form': form})

@csrf_protect
@sanitize_input
def recuperar_password_view(request):
    if request.method == 'POST':
        email = request.POST.get('email', '').strip()
        if not email:
            messages.error(request, 'Por favor, ingrese su correo electrónico')
            return render(request, 'tienda/recuperar_password.html')
            
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

@csrf_protect
@sanitize_input
def restablecer_password_view(request, token):
    try:
        token_recuperacion = TokenRecuperacion.objects.get(
            token=token,
            fecha_expiracion__gt=timezone.now()
        )
        
        if request.method == 'POST':
            password1 = request.POST.get('password1', '').strip()
            password2 = request.POST.get('password2', '').strip()
            
            if not password1 or not password2:
                messages.error(request, 'Por favor, complete todos los campos')
                return render(request, 'tienda/restablecer_password.html')
                
            if password1 != password2:
                messages.error(request, 'Las contraseñas no coinciden')
                return render(request, 'tienda/restablecer_password.html')
            
            if len(password1) < 8:
                messages.error(request, 'La contraseña debe tener al menos 8 caracteres')
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

def detalle_juego(request, juego_id):
    juego = get_object_or_404(Juego, id=juego_id)
    return render(request, 'tienda/detalle_juego.html', {'juego': juego})

def agregar_al_carrito(request, juego_id):
    if not request.user.is_authenticated:
        return redirect('tienda:login')
    
    juego = get_object_or_404(Juego, id=juego_id)
    carrito, created = Carrito.objects.get_or_create(usuario=request.user)
    
    # Verificar si el juego ya está en el carrito
    carrito_item, created = CarritoItem.objects.get_or_create(
        carrito=carrito,
        producto=juego,
        defaults={'cantidad': 1, 'precio_unitario': juego.precio}
    )
    
    if not created:
        carrito_item.cantidad += 1
        carrito_item.save()
    
    return redirect('tienda:carrito') 