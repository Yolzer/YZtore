from django.core.exceptions import ValidationError
from django.utils import timezone
from django.core.mail import send_mail
from django.conf import settings
from django.utils.crypto import get_random_string
from datetime import timedelta
from .models import Producto, Carrito, CarritoItem, TokenRecuperacion, CustomUser
from django.core.cache import cache
from django.db.models import Prefetch, F, Sum
from .utils import (
    enviar_correo_recuperacion,
    validar_telefono,
    calcular_precio_con_descuento,
    obtener_fecha_expiracion_token,
    sanitizar_input
)

class ProductoService:
    """Servicio para manejar operaciones relacionadas con productos."""
    
    @staticmethod
    def obtener_productos_destacados(limit=3):
        """
        Obtiene los productos destacados con sus relaciones optimizadas.
        
        Args:
            limit: Número máximo de productos a retornar
            
        Returns:
            QuerySet: Productos destacados con relaciones cargadas
        """
        return Producto.objects.select_related('categoria').prefetch_related(
            Prefetch('carritoitem_set', queryset=CarritoItem.objects.select_related('carrito'))
        ).filter(destacado=True)[:limit]

    @staticmethod
    def obtener_productos_ofertas(limit=3):
        """
        Obtiene los productos en oferta con sus relaciones optimizadas.
        
        Args:
            limit: Número máximo de productos a retornar
            
        Returns:
            QuerySet: Productos en oferta con relaciones cargadas
        """
        return Producto.objects.select_related('categoria').prefetch_related(
            Prefetch('carritoitem_set', queryset=CarritoItem.objects.select_related('carrito'))
        ).filter(descuento__gt=0)[:limit]

    @staticmethod
    def filtrar_productos(categoria=None, orden='recientes'):
        """
        Filtra y ordena productos según los criterios especificados.
        
        Args:
            categoria: Categoría para filtrar (opcional)
            orden: Criterio de ordenamiento ('recientes', 'precio_asc', 'precio_desc', 'nombre')
            
        Returns:
            QuerySet: Productos filtrados y ordenados
        """
        queryset = Producto.objects.select_related('categoria').prefetch_related(
            Prefetch('carritoitem_set', queryset=CarritoItem.objects.select_related('carrito'))
        )
        
        if categoria:
            queryset = queryset.filter(categoria=categoria)
        
        if orden == 'precio_asc':
            queryset = queryset.order_by('precio')
        elif orden == 'precio_desc':
            queryset = queryset.order_by('-precio')
        elif orden == 'nombre':
            queryset = queryset.order_by('nombre')
        else:
            queryset = queryset.order_by('-fecha_creacion')
        
        return queryset

class CarritoService:
    """Servicio para manejar operaciones relacionadas con el carrito de compras."""
    
    @staticmethod
    def obtener_carrito_usuario(usuario):
        """
        Obtiene o crea el carrito de un usuario con sus relaciones optimizadas.
        
        Args:
            usuario: Instancia del modelo CustomUser
            
        Returns:
            Carrito: Carrito del usuario con sus items cargados
        """
        carrito, created = Carrito.objects.select_related('usuario').prefetch_related(
            Prefetch('carritoitem_set', 
                    queryset=CarritoItem.objects.select_related('producto')
            )
        ).get_or_create(usuario=usuario)
        return carrito

    @staticmethod
    def agregar_producto_carrito(usuario, producto_id, cantidad=1):
        """
        Agrega un producto al carrito del usuario.
        
        Args:
            usuario: Instancia del modelo CustomUser
            producto_id: ID del producto a agregar
            cantidad: Cantidad del producto (default: 1)
            
        Returns:
            CarritoItem: Item del carrito creado o actualizado
        """
        producto = Producto.objects.select_related('categoria').get(id=producto_id)
        carrito = CarritoService.obtener_carrito_usuario(usuario)
        
        carrito_item, created = CarritoItem.objects.select_related('producto').get_or_create(
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
        """
        Calcula el total del carrito de manera eficiente.
        
        Args:
            carrito: Instancia del modelo Carrito
            
        Returns:
            float: Total del carrito
        """
        return CarritoItem.objects.filter(carrito=carrito).aggregate(
            total=Sum(F('cantidad') * F('precio_unitario'))
        )['total'] or 0

class UsuarioService:
    """Servicio para manejar operaciones relacionadas con usuarios."""
    
    @staticmethod
    def generar_token_recuperacion(usuario):
        """
        Genera un token de recuperación para un usuario.
        
        Args:
            usuario: Instancia del modelo CustomUser
            
        Returns:
            TokenRecuperacion: Token generado
        """
        token = get_random_string(length=32)
        token_recuperacion, created = TokenRecuperacion.objects.update_or_create(
            user=usuario,
            defaults={
                'token': token,
                'fecha_expiracion': obtener_fecha_expiracion_token()
            }
        )
        return token_recuperacion

    @staticmethod
    def enviar_correo_recuperacion(usuario, token, reset_url):
        """
        Envía el correo de recuperación de contraseña.
        
        Args:
            usuario: Instancia del modelo CustomUser
            token: Token de recuperación
            reset_url: URL completa para restablecer la contraseña
        """
        enviar_correo_recuperacion(usuario, token, reset_url)

    @staticmethod
    def validar_token_recuperacion(token):
        """
        Valida un token de recuperación.
        
        Args:
            token: Token a validar
            
        Returns:
            TokenRecuperacion: Token válido o None si no es válido
        """
        try:
            token_recuperacion = TokenRecuperacion.objects.get(
                token=token,
                fecha_expiracion__gt=timezone.now()
            )
            return token_recuperacion
        except TokenRecuperacion.DoesNotExist:
            return None 