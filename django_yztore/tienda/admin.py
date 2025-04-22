from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group
from .models import PerfilUsuario, Role, CustomUser

class PerfilUsuarioInline(admin.StackedInline):
    model = PerfilUsuario
    can_delete = False
    verbose_name_plural = 'Perfil'

class CustomUserAdmin(UserAdmin):
    inlines = (PerfilUsuarioInline,)
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'get_role')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    ordering = ('username',)

    def get_role(self, obj):
        try:
            return obj.perfilusuario.rol
        except:
            return 'No definido'
    get_role.short_description = 'Rol'

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