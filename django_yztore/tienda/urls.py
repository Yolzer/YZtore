from django.urls import path
from . import views

app_name = 'tienda'

urlpatterns = [
    path('', views.inicio, name='inicio'),
    path('login/', views.login_view, name='login'),
    path('registro/', views.registro_view, name='registro'),
    path('logout/', views.logout_view, name='logout'),
    path('recuperar-password/', views.recuperar_password_view, name='recuperar_password'),
    path('restablecer-password/<str:token>/', views.restablecer_password_view, name='restablecer_password'),
    path('juegos/', views.juegos_view, name='juegos'),
    path('ofertas/', views.ofertas_view, name='ofertas'),
    path('carrito/', views.carrito_view, name='carrito'),
    path('perfil/', views.perfil, name='perfil'),
] 