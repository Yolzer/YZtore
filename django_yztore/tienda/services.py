from django.core.exceptions import ValidationError
from django.utils import timezone
from django.core.mail import send_mail
from django.conf import settings
from django.utils.crypto import get_random_string
from datetime import timedelta
from .models import Producto, Carrito, CarritoItem, TokenRecuperacion, CustomUser

class ProductoService:
    @staticmethod
    def obtener_productos_destacados(limit=3):
        return Producto.objects.filter(destacado=True)[:limit]

    @staticmethod
    def obtener_productos_ofertas(limit=3):
        return Producto.objects.filter(descuento__gt=0)[:limit]

    @staticmethod
    def filtrar_productos(categoria=None, orden='recientes'):
        productos = Producto.objects.all()
        
        if categoria:
            productos = productos.filter(categoria=categoria)
        
        if orden == 'precio_asc':
            productos = productos.order_by('precio')
        elif orden == 'precio_desc':
            productos = productos.order_by('-precio')
        elif orden == 'nombre':
            productos = productos.order_by('nombre')
        else:
            productos = productos.order_by('-fecha_creacion')
        
        return productos

class CarritoService:
    @staticmethod
    def obtener_carrito_usuario(usuario):
        carrito, created = Carrito.objects.get_or_create(usuario=usuario)
        return carrito

    @staticmethod
    def agregar_producto_carrito(usuario, producto_id, cantidad=1):
        producto = Producto.objects.get(id=producto_id)
        carrito = CarritoService.obtener_carrito_usuario(usuario)
        
        carrito_item, created = CarritoItem.objects.get_or_create(
            carrito=carrito,
            producto=producto,
            defaults={'cantidad': cantidad, 'precio_unitario': producto.precio}
        )
        
        if not created:
            carrito_item.cantidad += cantidad
            carrito_item.save()
        
        return carrito_item

    @staticmethod
    def calcular_total_carrito(carrito):
        items = CarritoItem.objects.filter(carrito=carrito)
        return sum(item.cantidad * item.precio_unitario for item in items)

class UsuarioService:
    @staticmethod
    def generar_token_recuperacion(usuario):
        token = get_random_string(length=32)
        token_recuperacion, created = TokenRecuperacion.objects.update_or_create(
            user=usuario,
            defaults={
                'token': token,
                'fecha_expiracion': timezone.now() + timedelta(hours=24)
            }
        )
        return token_recuperacion

    @staticmethod
    def enviar_correo_recuperacion(usuario, token, reset_url):
        send_mail(
            'Recuperación de Contraseña - YZtore',
            f'Para restablecer tu contraseña, haz clic en el siguiente enlace: {reset_url}',
            settings.EMAIL_HOST_USER,
            [usuario.email],
            fail_silently=False,
        )

    @staticmethod
    def validar_token_recuperacion(token):
        try:
            token_recuperacion = TokenRecuperacion.objects.get(
                token=token,
                fecha_expiracion__gt=timezone.now()
            )
            return token_recuperacion
        except TokenRecuperacion.DoesNotExist:
            return None 