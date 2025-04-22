from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group
from .models import PerfilUsuario, Role, CustomUser, Juego, TokenRecuperacion

class PerfilUsuarioInline(admin.StackedInline):
    model = PerfilUsuario
    can_delete = False
    verbose_name_plural = 'Perfil'

class CustomUserAdmin(UserAdmin):
    inlines = (PerfilUsuarioInline,)
    list_display = ('email', 'username', 'first_name', 'last_name', 'is_staff')
    search_fields = ('email', 'username', 'first_name', 'last_name')
    ordering = ('email',)

@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'descripcion')
    search_fields = ('nombre',)
    ordering = ('nombre',)

# Registrar el modelo CustomUser con el admin personalizado
admin.site.register(CustomUser, CustomUserAdmin)

# Desregistrar el modelo Group original y registrar uno personalizado
admin.site.unregister(Group)

@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = ('name', 'get_users_count')
    search_fields = ('name',)
    ordering = ('name',)

    def get_users_count(self, obj):
        return obj.user_set.count()
    get_users_count.short_description = 'Usuarios'

admin.site.register(Juego)
admin.site.register(TokenRecuperacion) 