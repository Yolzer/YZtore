from django.core.exceptions import ValidationError
import re

def validar_password(password):
    """
    Valida que la contraseña cumpla con los siguientes requisitos:
    - Mínimo 8 caracteres
    - Máximo 20 caracteres
    - Al menos una letra mayúscula
    - Al menos una letra minúscula
    - Al menos un número
    - Al menos un carácter especial
    """
    if len(password) < 8:
        raise ValidationError("La contraseña debe tener al menos 8 caracteres.")
    if len(password) > 20:
        raise ValidationError("La contraseña no puede tener más de 20 caracteres.")
    if not re.search(r'[A-Z]', password):
        raise ValidationError("La contraseña debe contener al menos una letra mayúscula.")
    if not re.search(r'[a-z]', password):
        raise ValidationError("La contraseña debe contener al menos una letra minúscula.")
    if not re.search(r'[0-9]', password):
        raise ValidationError("La contraseña debe contener al menos un número.")
    if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
        raise ValidationError("La contraseña debe contener al menos un carácter especial.")

def validar_telefono(telefono):
    """
    Valida que el número de teléfono tenga el formato correcto
    """
    if not re.match(r'^\+?1?\d{9,15}$', telefono):
        raise ValidationError("El número de teléfono no tiene un formato válido.")

def validar_fecha_nacimiento(fecha):
    """
    Valida que la fecha de nacimiento sea válida
    """
    from datetime import date
    if fecha > date.today():
        raise ValidationError("La fecha de nacimiento no puede ser futura.")
    edad = (date.today() - fecha).days / 365
    if edad < 13:
        raise ValidationError("Debes tener al menos 13 años para registrarte.") 