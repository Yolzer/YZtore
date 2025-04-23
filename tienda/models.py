from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from decimal import Decimal
from django.utils import timezone

# Create your models here.

class Perfil(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    direccion = models.CharField(max_length=200)
    telefono = models.CharField(max_length=20)
    fecha_nacimiento = models.DateField()
    
    def __str__(self):
        return f"{self.usuario.username}"

class Categoria(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True)
    imagen = models.ImageField(upload_to='categorias/', blank=True, null=True)
    activo = models.BooleanField(default=True)
    fecha_creacion = models.DateTimeField(default=timezone.now)

    class Meta:
        verbose_name = 'Categoría'
        verbose_name_plural = 'Categorías'
        ordering = ['nombre']

    def __str__(self):
        return self.nombre

class Producto(models.Model):
    nombre = models.CharField(max_length=200)
    descripcion = models.TextField()
    precio = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(Decimal('0.01'))])
    imagen = models.ImageField(upload_to='productos/')
    stock = models.PositiveIntegerField(default=0)
    categoria = models.ForeignKey(Categoria, on_delete=models.SET_NULL, null=True, related_name='productos')
    destacado = models.BooleanField(default=False)
    activo = models.BooleanField(default=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Producto'
        verbose_name_plural = 'Productos'
        ordering = ['-fecha_creacion']

    def __str__(self):
        return self.nombre

    @property
    def disponible(self):
        return self.stock > 0

class Carrito(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    activo = models.BooleanField(default=True)
    
    def __str__(self):
        return f"Carrito de {self.usuario.username}"

class ItemCarrito(models.Model):
    carrito = models.ForeignKey(Carrito, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.IntegerField(validators=[MinValueValidator(1)])
    
    def __str__(self):
        return f"{self.cantidad} x {self.producto.nombre}"

class Orden(models.Model):
    ESTADOS = [
        ('P', 'Pendiente'),
        ('C', 'Completada'),
        ('A', 'Cancelada'),
    ]
    
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    estado = models.CharField(max_length=1, choices=ESTADOS, default='P')
    total = models.DecimalField(max_digits=10, decimal_places=2)
    
    def __str__(self):
        return f"Orden #{self.id} - {self.usuario.username}"

class ItemOrden(models.Model):
    orden = models.ForeignKey(Orden, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.IntegerField(validators=[MinValueValidator(1)])
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)
    
    def __str__(self):
        return f"{self.cantidad} x {self.producto.nombre}"

class ClienteNoRegistrado(models.Model):
    nombre = models.CharField(max_length=100)
    email = models.EmailField()
    rut = models.CharField(max_length=12)
    direccion = models.TextField()
    telefono = models.CharField(max_length=20)
    metodo_pago = models.CharField(max_length=20, choices=[
        ('transferencia', 'Transferencia Bancaria'),
        ('tarjeta', 'Tarjeta de Crédito/Débito')
    ])
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    orden = models.OneToOneField('Orden', on_delete=models.CASCADE, related_name='cliente_no_registrado')

    def __str__(self):
        return f"{self.nombre} - {self.email}"
