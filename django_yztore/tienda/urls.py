from django.urls import path
from . import views

app_name = 'tienda'

urlpatterns = [
    path('', views.inicio, name='inicio'),
    path('juegos/', views.juegos_view, name='juegos'),
    path('ofertas/', views.ofertas_view, name='ofertas'),
    path('carrito/', views.carrito_view, name='carrito'),
    path('login/', views.login_view, name='login'),
    path('registro/', views.registro, name='registro'),
    path('logout/', views.logout_view, name='logout'),
    path('perfil/', views.perfil, name='perfil'),
    path('juego/<int:juego_id>/', views.detalle_juego, name='detalle_juego'),
    path('agregar-al-carrito/<int:juego_id>/', views.agregar_al_carrito, name='agregar_al_carrito'),
    path('recuperar-password/', views.recuperar_password_view, name='recuperar_password'),
    path('restablecer-password/<str:token>/', views.restablecer_password_view, name='restablecer_password'),
    # URLs de administración
    path('admin/usuarios/', views.gestion_usuarios, name='gestion_usuarios'),
    path('admin/usuarios/<int:user_id>/cambiar-rol/', views.cambiar_rol_usuario, name='cambiar_rol_usuario'),
] 