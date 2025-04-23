from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordResetForm, SetPasswordForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from .models import Perfil, Producto, Categoria

class RegistroForm(UserCreationForm):
    email = forms.EmailField(required=True)
    direccion = forms.CharField(max_length=200, required=True)
    telefono = forms.CharField(max_length=20, required=True)
    fecha_nacimiento = forms.DateField(required=True, widget=forms.DateInput(attrs={'type': 'date'}))

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'first_name', 'last_name', 'direccion', 'telefono', 'fecha_nacimiento']

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        
        # Validaciones de contraseña
        if len(password1) < 8:
            raise ValidationError("La contraseña debe tener al menos 8 caracteres.")
        if not any(c.isupper() for c in password1):
            raise ValidationError("La contraseña debe contener al menos una letra mayúscula.")
        if not any(c.islower() for c in password1):
            raise ValidationError("La contraseña debe contener al menos una letra minúscula.")
        if not any(c.isdigit() for c in password1):
            raise ValidationError("La contraseña debe contener al menos un número.")
        if not any(c in '!@#$%^&*()_+-=[]{}|;:,.<>?' for c in password1):
            raise ValidationError("La contraseña debe contener al menos un carácter especial.")
        
        if password1 and password2 and password1 != password2:
            raise ValidationError("Las contraseñas no coinciden.")
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
            perfil = Perfil.objects.create(
                usuario=user,
                direccion=self.cleaned_data['direccion'],
                telefono=self.cleaned_data['telefono'],
                fecha_nacimiento=self.cleaned_data['fecha_nacimiento']
            )
        return user

class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))

class PerfilForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']

class PerfilExtraForm(forms.ModelForm):
    class Meta:
        model = Perfil
        fields = ['direccion', 'telefono', 'fecha_nacimiento']
        widgets = {
            'fecha_nacimiento': forms.DateInput(attrs={'type': 'date'}),
        }

class CustomPasswordResetForm(PasswordResetForm):
    email = forms.EmailField(
        max_length=254,
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'})
    )

class CustomSetPasswordForm(SetPasswordForm):
    new_password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Nueva contraseña'})
    )
    new_password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirmar nueva contraseña'})
    )

class CategoriaForm(forms.ModelForm):
    class Meta:
        model = Categoria
        fields = ['nombre', 'descripcion', 'imagen', 'activo']
        widgets = {
            'descripcion': forms.Textarea(attrs={'rows': 3}),
        }

class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = ['nombre', 'descripcion', 'precio', 'imagen', 'stock', 'categoria', 'destacado', 'activo']
        widgets = {
            'descripcion': forms.Textarea(attrs={'rows': 3}),
            'precio': forms.NumberInput(attrs={'step': '0.01'}),
        }

    def clean_precio(self):
        precio = self.cleaned_data.get('precio')
        if precio <= 0:
            raise ValidationError("El precio debe ser mayor que 0")
        return precio

    def clean_stock(self):
        stock = self.cleaned_data.get('stock')
        if stock < 0:
            raise ValidationError("El stock no puede ser negativo")
        return stock 