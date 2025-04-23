from django.contrib import admin
from .models import Perfil, Categoria, Producto, Carrito, ItemCarrito, Orden, ItemOrden

@admin.register(Perfil)
class PerfilAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'telefono', 'direccion')
    search_fields = ('usuario__username', 'telefono')

@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('nombre',)
    search_fields = ('nombre',)

@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'precio', 'stock', 'categoria')
    list_filter = ('categoria',)
    search_fields = ('nombre', 'descripcion')

@admin.register(Carrito)
class CarritoAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'fecha_creacion', 'activo')
    list_filter = ('activo',)
    search_fields = ('usuario__username',)

@admin.register(ItemCarrito)
class ItemCarritoAdmin(admin.ModelAdmin):
    list_display = ('carrito', 'producto', 'cantidad')
    list_filter = ('carrito__activo',)

@admin.register(Orden)
class OrdenAdmin(admin.ModelAdmin):
    list_display = ('id', 'usuario', 'fecha_creacion', 'estado', 'total')
    list_filter = ('estado',)
    search_fields = ('usuario__username',)

@admin.register(ItemOrden)
class ItemOrdenAdmin(admin.ModelAdmin):
    list_display = ('orden', 'producto', 'cantidad', 'precio_unitario')
    search_fields = ('orden__id', 'producto__nombre')
