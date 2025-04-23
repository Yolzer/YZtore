from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager, User, Group
from django.utils.translation import gettext_lazy as _
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from django.utils import timezone
from decimal import Decimal

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('El email es obligatorio')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)

class Role(models.Model):
    nombre = models.CharField(max_length=50, unique=True)
    descripcion = models.TextField(default='', blank=True)

    def __str__(self):
        return self.nombre

    class Meta:
        db_table = 'roles'

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=150, unique=True)
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=150, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)
    fecha_registro = models.DateTimeField(default=timezone.now)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email

class Categoria(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'categorias'
        verbose_name = 'Categoría'
        verbose_name_plural = 'Categorías'

    def __str__(self):
        return self.nombre

class Producto(models.Model):
    TIPO_CHOICES = [
        ('juego', 'Juego'),
        ('consola', 'Consola'),
        ('accesorio', 'Accesorio'),
    ]

    CATEGORIA_CHOICES = [
        ('accion', 'Acción'),
        ('aventura', 'Aventura'),
        ('rpg', 'RPG'),
        ('estrategia', 'Estrategia'),
        ('deportes', 'Deportes'),
        ('simulacion', 'Simulación'),
    ]

    nombre = models.CharField(max_length=255)
    descripcion = models.TextField()
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    precio_original = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    descuento = models.IntegerField(default=0)
    stock = models.IntegerField(default=0)
    imagen = models.ImageField(upload_to='productos/', null=True, blank=True)
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES, default='juego')
    categoria = models.CharField(max_length=20, choices=CATEGORIA_CHOICES, default='accion')
    destacado = models.BooleanField(default=False)
    plataforma = models.CharField(max_length=50)
    fecha_creacion = models.DateTimeField(default=timezone.now)
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'productos'
        ordering = ['-fecha_creacion']
        verbose_name = 'Producto'
        verbose_name_plural = 'Productos'

    def __str__(self):
        return self.nombre

    @property
    def precio_con_descuento(self):
        if self.descuento > 0 and self.precio_original:
            descuento_decimal = Decimal(str(self.descuento)) / Decimal('100')
            return self.precio_original * (Decimal('1') - descuento_decimal)
        return self.precio

    def actualizar_stock(self, cantidad):
        """Actualiza el stock del producto de manera segura"""
        if self.stock + cantidad < 0:
            raise ValueError("No hay suficiente stock disponible")
        self.stock += cantidad
        self.save()

class Carrito(models.Model):
    usuario = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'carritos'

class CarritoItem(models.Model):
    carrito = models.ForeignKey(Carrito, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.IntegerField(default=1)
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'carrito_items'

class Pedido(models.Model):
    ESTADO_CHOICES = [
        ('pendiente', 'Pendiente'),
        ('pagado', 'Pagado'),
        ('enviado', 'Enviado'),
        ('entregado', 'Entregado'),
        ('cancelado', 'Cancelado'),
    ]

    usuario = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    estado = models.CharField(max_length=50, choices=ESTADO_CHOICES, default='pendiente')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'pedidos'

class PedidoItem(models.Model):
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.IntegerField()
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'pedido_items'

class TokenRecuperacion(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    token = models.CharField(max_length=100, unique=True)
    fecha_creacion = models.DateTimeField(default=timezone.now)
    fecha_expiracion = models.DateTimeField()

    def __str__(self):
        return f"Token para {self.user.username}"

class PerfilUsuario(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    rol = models.ForeignKey(Role, on_delete=models.SET_NULL, null=True)
    telefono = models.CharField(max_length=15, blank=True)
    direccion = models.TextField(blank=True)
    fecha_nacimiento = models.DateField(null=True, blank=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Perfil de {self.user.username}"

@receiver(post_save, sender=CustomUser)
def crear_perfil_usuario(sender, instance, created, **kwargs):
    if created:
        PerfilUsuario.objects.create(user=instance)

@receiver(post_save, sender=CustomUser)
def guardar_perfil_usuario(sender, instance, **kwargs):
    try:
        instance.perfilusuario.save()
    except PerfilUsuario.DoesNotExist:
        PerfilUsuario.objects.create(user=instance)

class Juego(models.Model):
    CATEGORIAS = [
        ('accion', 'Acción'),
        ('aventura', 'Aventura'),
        ('rpg', 'RPG'),
        ('estrategia', 'Estrategia'),
    ]

    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(default='', blank=True)
    precio = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    categoria = models.CharField(max_length=20, choices=CATEGORIAS, default='accion')
    imagen = models.CharField(max_length=500, default='', blank=True)
    destacado = models.BooleanField(default=False)
    descuento = models.IntegerField(default=0)
    precio_original = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    fecha_creacion = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.nombre

    @property
    def precio_con_descuento(self):
        if self.descuento > 0 and self.precio_original:
            descuento_decimal = Decimal(str(self.descuento)) / Decimal('100')
            return self.precio_original * (Decimal('1') - descuento_decimal)
        return self.precio

    class Meta:
        db_table = 'juegos'
        ordering = ['-fecha_creacion'] 