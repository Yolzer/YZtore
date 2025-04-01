// Datos de ejemplo de productos
const productos = [
    {
        id: 1,
        nombre: "The Witcher 3: Wild Hunt",
        precio: 29.99,
        imagen: "img/productos/witcher3.jpg",
        plataforma: "GOG",
        descripcion: "El RPG de fantasía más aclamado de la década",
        stock: 15
    },
    {
        id: 2,
        nombre: "Cyberpunk 2077",
        precio: 39.99,
        imagen: "img/productos/cyberpunk.jpg",
        plataforma: "GOG",
        descripcion: "RPG de acción y aventura futurista",
        stock: 8
    },
    {
        id: 3,
        nombre: "Red Dead Redemption 2",
        precio: 59.99,
        imagen: "img/productos/rdr2.jpg",
        plataforma: "Epic Games",
        descripcion: "Aventura del Salvaje Oeste",
        stock: 5
    }
];

// Carrito de compras
let carrito = JSON.parse(localStorage.getItem('carrito')) || [];

// Función para mostrar productos en la página
function mostrarProductos() {
    const contenedor = document.getElementById('featured-products');
    contenedor.innerHTML = '';
    
    productos.forEach(producto => {
        const productoHTML = `
            <div class="col-md-4">
                <div class="card product-card">
                    <img src="${producto.imagen}" class="card-img-top" alt="${producto.nombre}">
                    <div class="card-body">
                        <h5 class="card-title">${producto.nombre}</h5>
                        <p class="card-text">${producto.descripcion}</p>
                        <p class="card-text"><small class="text-muted">Plataforma: ${producto.plataforma}</small></p>
                        <div class="d-flex justify-content-between align-items-center">
                            <span class="product-price">$${producto.precio}</span>
                            <button class="btn btn-primary" onclick="agregarAlCarrito(${producto.id})" 
                                    ${producto.stock === 0 ? 'disabled' : ''}>
                                <i class="fas fa-shopping-cart"></i> Comprar
                            </button>
                        </div>
                        <small class="text-muted">Stock disponible: ${producto.stock}</small>
                    </div>
                </div>
            </div>
        `;
        contenedor.innerHTML += productoHTML;
    });
}

// Función para agregar productos al carrito
function agregarAlCarrito(id) {
    const producto = productos.find(p => p.id === id);
    if (producto && producto.stock > 0) {
        const itemEnCarrito = carrito.find(item => item.id === id);
        
        if (itemEnCarrito) {
            if (itemEnCarrito.cantidad < producto.stock) {
                itemEnCarrito.cantidad++;
                itemEnCarrito.subtotal = itemEnCarrito.cantidad * producto.precio;
            } else {
                alert('No hay suficiente stock disponible.');
            }
        } else {
            carrito.push({
                id: producto.id,
                nombre: producto.nombre,
                precio: producto.precio,
                cantidad: 1,
                subtotal: producto.precio
            });
        }
        
        actualizarCarrito();
        localStorage.setItem('carrito', JSON.stringify(carrito));
    }
}

// Función para actualizar la vista del carrito
function actualizarCarrito() {
    const contenedor = document.getElementById('carritoItems');
    const contador = document.getElementById('carritoCantidad');
    const total = document.getElementById('carritoTotal');
    
    contenedor.innerHTML = '';
    let totalCarrito = 0;
    let cantidadTotal = 0;
    
    carrito.forEach(item => {
        const itemHTML = `
            <div class="d-flex justify-content-between align-items-center mb-2">
                <div>
                    <h6 class="mb-0">${item.nombre}</h6>
                    <small class="text-muted">$${item.precio} x ${item.cantidad}</small>
                    <br>
                    <small class="text-primary">Subtotal: $${item.subtotal.toFixed(2)}</small>
                </div>
                <div>
                    <button class="btn btn-sm btn-outline-danger" onclick="eliminarDelCarrito(${item.id})">
                        <i class="fas fa-trash"></i>
                    </button>
                    <button class="btn btn-sm btn-outline-secondary" onclick="actualizarCantidad(${item.id}, -1)">-</button>
                    <span class="mx-2">${item.cantidad}</span>
                    <button class="btn btn-sm btn-outline-secondary" onclick="actualizarCantidad(${item.id}, 1)">+</button>
                </div>
            </div>
        `;
        contenedor.innerHTML += itemHTML;
        totalCarrito += item.subtotal;
        cantidadTotal += item.cantidad;
    });
    
    contador.textContent = cantidadTotal;
    total.textContent = totalCarrito.toFixed(2);
}

// Función para eliminar items del carrito
function eliminarDelCarrito(id) {
    carrito = carrito.filter(item => item.id !== id);
    actualizarCarrito();
    localStorage.setItem('carrito', JSON.stringify(carrito));
}

// Función para actualizar cantidad en el carrito
function actualizarCantidad(id, cambio) {
    const item = carrito.find(item => item.id === id);
    if (item) {
        const producto = productos.find(p => p.id === id);
        const nuevaCantidad = item.cantidad + cambio;
        
        if (nuevaCantidad > 0 && nuevaCantidad <= producto.stock) {
            item.cantidad = nuevaCantidad;
            item.subtotal = item.cantidad * item.precio;
            actualizarCarrito();
            localStorage.setItem('carrito', JSON.stringify(carrito));
        }
    }
}

// Función para proceder al pago
function procederAlPago() {
    const usuario = JSON.parse(sessionStorage.getItem('usuario'));
    if (!usuario) {
        alert('Por favor, inicia sesión para continuar con la compra.');
        window.location.href = 'login.html';
        return;
    }
    
    if (carrito.length === 0) {
        alert('Tu carrito está vacío.');
        return;
    }
    
    // Aquí se implementaría la lógica de pago
    alert('¡Compra realizada con éxito!');
    carrito = [];
    actualizarCarrito();
    localStorage.setItem('carrito', JSON.stringify(carrito));
    
    // Cerrar el modal del carrito
    const modal = bootstrap.Modal.getInstance(document.getElementById('carritoModal'));
    modal.hide();
}

// Inicializar la página
document.addEventListener('DOMContentLoaded', () => {
    mostrarProductos();
    actualizarCarrito();
    
    // Verificar si el usuario está autenticado
    const usuario = JSON.parse(sessionStorage.getItem('usuario'));
    if (usuario) {
        document.getElementById('btnLogin').innerHTML = `
            <i class="fas fa-user"></i> ${usuario.nombre}
        `;
    }
}); 