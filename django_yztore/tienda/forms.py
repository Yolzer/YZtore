from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from .validators import validar_password, validar_telefono, validar_fecha_nacimiento, sanitize_input
from .models import CustomUser, PerfilUsuario
from .utils import sanitizar_input

class RegistroForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={'class': 'form-control'})
    )
    telefono = forms.CharField(
        max_length=15,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    fecha_nacimiento = forms.DateField(
        required=True,
        widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'})
    )
    direccion = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        required=True
    )

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'password1', 'password2', 'telefono', 'fecha_nacimiento', 'direccion')

    def clean_username(self):
        username = sanitize_input(self.cleaned_data.get('username'))
        if CustomUser.objects.filter(username=username).exists():
            raise ValidationError('Este nombre de usuario ya está en uso.')
        return username

    def clean_email(self):
        email = sanitize_input(self.cleaned_data.get('email'))
        if CustomUser.objects.filter(email=email).exists():
            raise ValidationError('Este correo electrónico ya está registrado.')
        return email

    def clean_password1(self):
        password = self.cleaned_data.get('password1')
        validar_password(password)
        return password

    def clean_telefono(self):
        telefono = self.cleaned_data.get('telefono')
        if not validar_telefono(telefono):
            raise ValidationError(_('Por favor ingrese un número de teléfono válido'))
        return telefono

    def clean_fecha_nacimiento(self):
        fecha = self.cleaned_data.get('fecha_nacimiento')
        validar_fecha_nacimiento(fecha)
        return fecha

    def clean_direccion(self):
        direccion = self.cleaned_data.get('direccion')
        return sanitizar_input(direccion)

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
            # Crear perfil de usuario
            PerfilUsuario.objects.create(
                user=user,
                telefono=self.cleaned_data['telefono'],
                fecha_nacimiento=self.cleaned_data['fecha_nacimiento'],
                direccion=self.cleaned_data['direccion']
            )
        return user

class PerfilForm(forms.ModelForm):
    class Meta:
        model = PerfilUsuario
        fields = ['telefono', 'direccion', 'fecha_nacimiento']
        widgets = {
            'fecha_nacimiento': forms.DateInput(attrs={'type': 'date'}),
            'direccion': forms.Textarea(attrs={'rows': 3}),
        }

    def clean_telefono(self):
        telefono = self.cleaned_data.get('telefono')
        if not validar_telefono(telefono):
            raise ValidationError(_('Por favor ingrese un número de teléfono válido'))
        return telefono

    def clean_direccion(self):
        direccion = self.cleaned_data.get('direccion')
        return sanitizar_input(direccion) 