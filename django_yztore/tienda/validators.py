from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
import re
from datetime import datetime, timedelta

def validar_password(password):
    """
    Valida que la contraseña cumpla con los requisitos de seguridad.
    """
    if len(password) < 8:
        raise ValidationError(
            _('La contraseña debe tener al menos 8 caracteres.')
        )
    if not re.search(r'[A-Z]', password):
        raise ValidationError(
            _('La contraseña debe contener al menos una letra mayúscula.')
        )
    if not re.search(r'[a-z]', password):
        raise ValidationError(
            _('La contraseña debe contener al menos una letra minúscula.')
        )
    if not re.search(r'[0-9]', password):
        raise ValidationError(
            _('La contraseña debe contener al menos un número.')
        )
    if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
        raise ValidationError(
            _('La contraseña debe contener al menos un carácter especial.')
        )

def validar_telefono(telefono):
    """
    Valida que el número de teléfono tenga un formato válido.
    """
    if not re.match(r'^\+?1?\d{9,15}$', telefono):
        raise ValidationError(
            _('El número de teléfono debe tener entre 9 y 15 dígitos.')
        )

def validar_fecha_nacimiento(fecha):
    """
    Valida que la fecha de nacimiento sea válida y que el usuario tenga al menos 13 años.
    """
    if fecha > datetime.now().date():
        raise ValidationError(
            _('La fecha de nacimiento no puede ser en el futuro.')
        )
    
    edad_minima = datetime.now().date() - timedelta(days=13*365)
    if fecha > edad_minima:
        raise ValidationError(
            _('Debes tener al menos 13 años para registrarte.')
        )

def sanitize_input(data):
    """
    Sanitiza los datos de entrada eliminando espacios en blanco y caracteres especiales peligrosos.
    """
    if isinstance(data, str):
        # Eliminar espacios en blanco al inicio y final
        data = data.strip()
        # Eliminar caracteres especiales peligrosos
        data = re.sub(r'[<>{}[\]]', '', data)
    return data 