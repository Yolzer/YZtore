from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .validators import validar_password, validar_telefono, validar_fecha_nacimiento

class RegistroForm(UserCreationForm):
    email = forms.EmailField(required=True)
    telefono = forms.CharField(max_length=15, required=True)
    fecha_nacimiento = forms.DateField(required=True)
    direccion = forms.CharField(widget=forms.Textarea, required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', 'telefono', 'fecha_nacimiento', 'direccion')

    def clean_password1(self):
        password = self.cleaned_data.get('password1')
        validar_password(password)
        return password

    def clean_telefono(self):
        telefono = self.cleaned_data.get('telefono')
        validar_telefono(telefono)
        return telefono

    def clean_fecha_nacimiento(self):
        fecha = self.cleaned_data.get('fecha_nacimiento')
        validar_fecha_nacimiento(fecha)
        return fecha

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
            # Crear perfil de usuario
            from .models import PerfilUsuario
            PerfilUsuario.objects.create(
                usuario=user,
                telefono=self.cleaned_data['telefono'],
                fecha_nacimiento=self.cleaned_data['fecha_nacimiento'],
                direccion=self.cleaned_data['direccion']
            )
        return user 