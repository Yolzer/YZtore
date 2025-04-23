from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate, update_session_auth_hash
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
from django.contrib import messages
from django.urls import reverse_lazy
from django.db.models import Q
from .forms import RegistroForm, LoginForm, CustomPasswordResetForm, CustomSetPasswordForm, PerfilForm, PerfilExtraForm, ProductoForm, CategoriaForm
from .models import Perfil, Producto, Categoria, Carrito, ItemCarrito, Orden, ClienteNoRegistrado, ItemOrden
from django.contrib.auth.forms import PasswordChangeForm

def inicio(request):
    productos_destacados = Producto.objects.all()[:8]
    categorias = Categoria.objects.all()
    return render(request, 'tienda/inicio.html', {
        'productos_destacados': productos_destacados,
        'categorias': categorias
    })

def catalogo(request):
    productos = Producto.objects.all()
    categorias = Categoria.objects.all()
    categoria_seleccionada = request.GET.get('categoria')
    
    if categoria_seleccionada:
        productos = productos.filter(categoria__id=categoria_seleccionada)
    
    return render(request, 'tienda/catalogo.html', {
        'productos': productos,
        'categorias': categorias,
        'categoria_seleccionada': categoria_seleccionada
    })

def detalle_producto(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)
    return render(request, 'tienda/detalle_producto.html', {'producto': producto})

def carrito(request):
    if request.user.is_authenticated:
        carrito, created = Carrito.objects.get_or_create(usuario=request.user, activo=True)
        items = ItemCarrito.objects.filter(carrito=carrito)
    else:
        carrito_id = request.session.get('carrito_id')
        if carrito_id:
            carrito = get_object_or_404(Carrito, id=carrito_id, activo=True)
            items = ItemCarrito.objects.filter(carrito=carrito)
        else:
            items = []
    
    total = sum(item.producto.precio * item.cantidad for item in items)
    
    return render(request, 'tienda/carrito.html', {
        'items': items,
        'total': total
    })

def agregar_al_carrito(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)
    
    if request.user.is_authenticated:
        carrito, created = Carrito.objects.get_or_create(usuario=request.user, activo=True)
    else:
        carrito_id = request.session.get('carrito_id')
        if carrito_id:
            carrito = get_object_or_404(Carrito, id=carrito_id, activo=True)
        else:
            carrito = Carrito.objects.create(activo=True)
            request.session['carrito_id'] = carrito.id
    
    item, created = ItemCarrito.objects.get_or_create(
        carrito=carrito,
        producto=producto,
        defaults={'cantidad': 1}
    )
    
    if not created:
        item.cantidad += 1
        item.save()
    
    messages.success(request, f'¡{producto.nombre} agregado al carrito!')
    return redirect('carrito')

def eliminar_del_carrito(request, item_id):
    if request.user.is_authenticated:
        item = get_object_or_404(ItemCarrito, id=item_id, carrito__usuario=request.user)
    else:
        carrito_id = request.session.get('carrito_id')
        if carrito_id:
            item = get_object_or_404(ItemCarrito, id=item_id, carrito__id=carrito_id)
        else:
            return redirect('carrito')
    
    item.delete()
    messages.success(request, 'Producto eliminado del carrito')
    return redirect('carrito')

def checkout(request):
    if request.user.is_authenticated:
        carrito = get_object_or_404(Carrito, usuario=request.user, activo=True)
    else:
        carrito_id = request.session.get('carrito_id')
        if carrito_id:
            carrito = get_object_or_404(Carrito, id=carrito_id, activo=True)
        else:
            return redirect('carrito')
    
    items = ItemCarrito.objects.filter(carrito=carrito)
    
    if not items.exists():
        messages.warning(request, 'Tu carrito está vacío')
        return redirect('carrito')
    
    total = sum(item.producto.precio * item.cantidad for item in items)
    
    if request.method == 'POST':
        if request.user.is_authenticated:
            orden = Orden.objects.create(
                usuario=request.user,
                total=total
            )
        else:
            # Crear orden sin usuario
            orden = Orden.objects.create(total=total)
            
            # Crear cliente no registrado
            ClienteNoRegistrado.objects.create(
                nombre=request.POST.get('nombre'),
                email=request.POST.get('email'),
                rut=request.POST.get('rut'),
                direccion=request.POST.get('direccion'),
                telefono=request.POST.get('telefono'),
                metodo_pago=request.POST.get('metodo_pago'),
                orden=orden
            )
        
        # Crear los items de la orden
        for item in items:
            ItemOrden.objects.create(
                orden=orden,
                producto=item.producto,
                cantidad=item.cantidad,
                precio_unitario=item.producto.precio
            )
        
        # Desactivar el carrito
        carrito.activo = False
        carrito.save()
        
        if not request.user.is_authenticated:
            del request.session['carrito_id']
        
        messages.success(request, '¡Pago exitoso! Gracias por tu compra.')
        return redirect('inicio')
    
    return render(request, 'tienda/checkout.html', {
        'items': items,
        'total': total,
        'user_authenticated': request.user.is_authenticated
    })

def registro(request):
    if request.method == 'POST':
        form = RegistroForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, '¡Registro exitoso! Bienvenido a YZStore.')
            return redirect('inicio')
    else:
        form = RegistroForm()
    return render(request, 'tienda/registro.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'¡Bienvenido {username}!')
                return redirect('inicio')
    else:
        form = LoginForm()
    return render(request, 'tienda/login.html', {'form': form})

@login_required
def logout_view(request):
    logout(request)
    messages.info(request, 'Has cerrado sesión exitosamente.')
    return redirect('inicio')

@login_required
def perfil(request):
    if request.method == 'POST':
        user_form = PerfilForm(request.POST, instance=request.user)
        perfil_form = PerfilExtraForm(request.POST, request.FILES, instance=request.user.perfil)
        
        if user_form.is_valid() and perfil_form.is_valid():
            user_form.save()
            perfil_form.save()
            messages.success(request, 'Perfil actualizado exitosamente.')
            return redirect('perfil')
    else:
        user_form = PerfilForm(instance=request.user)
        perfil_form = PerfilExtraForm(instance=request.user.perfil)
    
    return render(request, 'tienda/perfil.html', {
        'user_form': user_form,
        'perfil_form': perfil_form
    })

@login_required
def historial_compras(request):
    ordenes = Orden.objects.filter(usuario=request.user).order_by('-fecha_creacion')
    return render(request, 'tienda/historial_compras.html', {'ordenes': ordenes})

@login_required
def detalle_orden(request, orden_id):
    orden = get_object_or_404(Orden, id=orden_id, usuario=request.user)
    items = ItemOrden.objects.filter(orden=orden)
    return render(request, 'tienda/detalle_orden.html', {
        'orden': orden,
        'items': items
    })

class CustomPasswordResetView(PasswordResetView):
    form_class = CustomPasswordResetForm
    template_name = 'tienda/password_reset.html'
    email_template_name = 'tienda/password_reset_email.html'
    success_url = reverse_lazy('password_reset_done')

class CustomPasswordResetDoneView(PasswordResetDoneView):
    template_name = 'tienda/password_reset_done.html'

class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    form_class = CustomSetPasswordForm
    template_name = 'tienda/password_reset_confirm.html'
    success_url = reverse_lazy('password_reset_complete')

class CustomPasswordResetCompleteView(PasswordResetCompleteView):
    template_name = 'tienda/password_reset_complete.html'

@permission_required('tienda.add_categoria')
def crear_categoria(request):
    if request.method == 'POST':
        form = CategoriaForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Categoría creada exitosamente')
            return redirect('lista_categorias')
    else:
        form = CategoriaForm()
    return render(request, 'tienda/categoria_form.html', {'form': form, 'titulo': 'Crear Categoría'})

@permission_required('tienda.change_categoria')
def editar_categoria(request, pk):
    categoria = get_object_or_404(Categoria, pk=pk)
    if request.method == 'POST':
        form = CategoriaForm(request.POST, request.FILES, instance=categoria)
        if form.is_valid():
            form.save()
            messages.success(request, 'Categoría actualizada exitosamente')
            return redirect('lista_categorias')
    else:
        form = CategoriaForm(instance=categoria)
    return render(request, 'tienda/categoria_form.html', {'form': form, 'titulo': 'Editar Categoría'})

@permission_required('tienda.delete_categoria')
def eliminar_categoria(request, pk):
    categoria = get_object_or_404(Categoria, pk=pk)
    if request.method == 'POST':
        categoria.delete()
        messages.success(request, 'Categoría eliminada exitosamente')
        return redirect('lista_categorias')
    return render(request, 'tienda/categoria_confirmar_eliminar.html', {'categoria': categoria})

@permission_required('tienda.add_producto')
def crear_producto(request):
    if request.method == 'POST':
        form = ProductoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Producto creado exitosamente')
            return redirect('lista_productos')
    else:
        form = ProductoForm()
    return render(request, 'tienda/producto_form.html', {'form': form, 'titulo': 'Crear Producto'})

@permission_required('tienda.change_producto')
def editar_producto(request, pk):
    producto = get_object_or_404(Producto, pk=pk)
    if request.method == 'POST':
        form = ProductoForm(request.POST, request.FILES, instance=producto)
        if form.is_valid():
            form.save()
            messages.success(request, 'Producto actualizado exitosamente')
            return redirect('lista_productos')
    else:
        form = ProductoForm(instance=producto)
    return render(request, 'tienda/producto_form.html', {'form': form, 'titulo': 'Editar Producto'})

@permission_required('tienda.delete_producto')
def eliminar_producto(request, pk):
    producto = get_object_or_404(Producto, pk=pk)
    if request.method == 'POST':
        producto.delete()
        messages.success(request, 'Producto eliminado exitosamente')
        return redirect('lista_productos')
    return render(request, 'tienda/producto_confirmar_eliminar.html', {'producto': producto})

def lista_productos(request):
    productos = Producto.objects.filter(activo=True)
    categorias = Categoria.objects.filter(activo=True)
    
    categoria_id = request.GET.get('categoria')
    if categoria_id:
        productos = productos.filter(categoria_id=categoria_id)
    
    busqueda = request.GET.get('q')
    if busqueda:
        productos = productos.filter(
            Q(nombre__icontains=busqueda) |
            Q(descripcion__icontains=busqueda)
        )
    
    return render(request, 'tienda/lista_productos.html', {
        'productos': productos,
        'categorias': categorias,
        'categoria_actual': int(categoria_id) if categoria_id else None,
        'busqueda': busqueda
    })

def lista_categorias(request):
    categorias = Categoria.objects.all()
    return render(request, 'tienda/lista_categorias.html', {'categorias': categorias})

@login_required
def cambiar_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Mantiene la sesión activa
            messages.success(request, '¡Tu contraseña ha sido actualizada!')
            return redirect('perfil')
        else:
            messages.error(request, 'Por favor corrige los errores.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'tienda/cambiar_password.html', {'form': form})
