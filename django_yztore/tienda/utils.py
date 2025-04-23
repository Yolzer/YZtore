from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone
from datetime import timedelta
from django.core.exceptions import ValidationError
import re

def enviar_correo_recuperacion(usuario, token, reset_url):
    """
    Envía un correo electrónico con el enlace para recuperar la contraseña.
    
    Args:
        usuario: Instancia del modelo CustomUser
        token: Token de recuperación
        reset_url: URL completa para restablecer la contraseña
    """
    send_mail(
        'Recuperación de Contraseña - YZtore',
        f'Para restablecer tu contraseña, haz clic en el siguiente enlace: {reset_url}',
        settings.EMAIL_HOST_USER,
        [usuario.email],
        fail_silently=False,
    )

def validar_telefono(telefono):
    """
    Valida el formato de un número de teléfono.
    
    Args:
        telefono: Número de teléfono a validar
        
    Returns:
        bool: True si el formato es válido, False en caso contrario
    """
    patron = r'^\+?1?\d{9,15}$'
    return bool(re.match(patron, telefono))

def calcular_precio_con_descuento(precio_original, descuento):
    """
    Calcula el precio final después de aplicar un descuento.
    
    Args:
        precio_original: Precio original del producto
        descuento: Porcentaje de descuento (0-100)
        
    Returns:
        float: Precio final con descuento aplicado
    """
    if descuento > 0:
        return precio_original * (1 - descuento/100)
    return precio_original

def obtener_fecha_expiracion_token(hours=24):
    """
    Genera una fecha de expiración para tokens.
    
    Args:
        hours: Número de horas hasta la expiración
        
    Returns:
        datetime: Fecha y hora de expiración
    """
    return timezone.now() + timedelta(hours=hours)

def sanitizar_input(texto):
    """
    Elimina caracteres peligrosos y espacios innecesarios de un texto.
    
    Args:
        texto: Texto a sanitizar
        
    Returns:
        str: Texto sanitizado
    """
    if not texto:
        return texto
    # Eliminar espacios al inicio y final
    texto = texto.strip()
    # Eliminar caracteres peligrosos
    texto = re.sub(r'[<>{}[\]]', '', texto)
    return texto 