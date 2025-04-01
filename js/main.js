// Datos de ejemplo de productos
const productos = [
    {
        id: 1,
        nombre: "The Witcher 3: Wild Hunt",
        precio: 29.99,
        imagen: "img/productos/witcher3.jpg",
        plataforma: "GOG",
        descripcion: "El RPG de fantasía más aclamado de la década. Explora un mundo abierto lleno de monstruos, misiones y decisiones que afectarán el destino de los reinos.",
        stock: 15
    },
    {
        id: 2,
        nombre: "Cyberpunk 2077",
        precio: 39.99,
        imagen: "img/productos/cyberpunk.jpg",
        plataforma: "GOG",
        descripcion: "RPG de acción y aventura futurista. Inmersión total en el mundo de Night City, donde la tecnología y la humanidad se fusionan.",
        stock: 8
    },
    {
        id: 3,
        nombre: "Red Dead Redemption 2",
        precio: 59.99,
        imagen: "img/productos/rdr2.jpg",
        plataforma: "Epic Games",
        descripcion: "Aventura del Salvaje Oeste. Vive la historia de Arthur Morgan y la banda Van der Linde en este épico juego de Rockstar Games.",
        stock: 5
    },
    {
        id: 4,
        nombre: "Monster Hunter Wilds",
        precio: 50.00,
        precioOriginal: 60.00,
        imagen: "img/productos/monster hunter wilds.jpg",
        plataforma: "Steam",
        descripcion: "La nueva entrega de la saga Monster Hunter. Caza monstruos gigantes en un mundo dinámico y peligroso.",
        stock: 12,
        descuento: 10
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

// Función para actualizar el contador del carrito en la barra de navegación
function actualizarContadorCarrito() {
    const contadorCarrito = document.getElementById('contadorCarrito');
    if (contadorCarrito) {
        const totalItems = carrito.reduce((total, item) => total + item.cantidad, 0);
        contadorCarrito.textContent = totalItems;
        contadorCarrito.style.display = totalItems > 0 ? 'block' : 'none';
    }
}

// Función para agregar productos al carrito
function agregarAlCarrito(id) {
    const producto = productos.find(p => p.id === id);
    if (!producto) return;

    const itemExistente = carrito.find(item => item.id === id);
    if (itemExistente) {
        if (itemExistente.cantidad < producto.stock) {
            itemExistente.cantidad++;
            itemExistente.subtotal = itemExistente.cantidad * producto.precio;
        } else {
            alert('No hay más unidades disponibles de este producto.');
            return;
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

    localStorage.setItem('carrito', JSON.stringify(carrito));
    actualizarContadorCarrito();
    alert('Producto agregado al carrito');
}

// Función para actualizar el carrito en la página del carrito
function actualizarCarrito() {
    const contenedor = document.getElementById('carritoItems');
    if (!contenedor) return;

    contenedor.innerHTML = '';
    if (carrito.length === 0) {
        contenedor.innerHTML = '<p class="text-center">Tu carrito está vacío</p>';
        return;
    }

    carrito.forEach(item => {
        const producto = productos.find(p => p.id === item.id);
        contenedor.innerHTML += `
            <div class="carrito-item mb-3">
                <div class="row align-items-center">
                    <div class="col-md-2">
                        <img src="${producto.imagen}" alt="${producto.nombre}" class="img-fluid">
                    </div>
                    <div class="col-md-4">
                        <h5>${producto.nombre}</h5>
                        <p class="text-muted">${producto.plataforma}</p>
                    </div>
                    <div class="col-md-2">
                        <div class="input-group">
                            <button class="btn btn-outline-secondary" onclick="actualizarCantidad(${item.id}, -1)">-</button>
                            <input type="number" class="form-control text-center" value="${item.cantidad}" readonly>
                            <button class="btn btn-outline-secondary" onclick="actualizarCantidad(${item.id}, 1)">+</button>
                        </div>
                    </div>
                    <div class="col-md-2">
                        <span>$${item.subtotal.toFixed(2)}</span>
                    </div>
                    <div class="col-md-2">
                        <button class="btn btn-danger" onclick="eliminarDelCarrito(${item.id})">
                            Eliminar
                        </button>
                    </div>
                </div>
            </div>
        `;
    });
}

// Función para actualizar la cantidad de un producto en el carrito
function actualizarCantidad(id, cambio) {
    const item = carrito.find(item => item.id === id);
    if (!item) return;

    const producto = productos.find(p => p.id === id);
    const nuevaCantidad = item.cantidad + cambio;

    if (nuevaCantidad > 0 && nuevaCantidad <= producto.stock) {
        item.cantidad = nuevaCantidad;
        item.subtotal = item.cantidad * producto.precio;
        localStorage.setItem('carrito', JSON.stringify(carrito));
        actualizarCarrito();
        actualizarResumen();
        actualizarContadorCarrito();
    }
}

// Función para eliminar un producto del carrito
function eliminarDelCarrito(id) {
    carrito = carrito.filter(item => item.id !== id);
    localStorage.setItem('carrito', JSON.stringify(carrito));
    actualizarCarrito();
    actualizarResumen();
    actualizarContadorCarrito();
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

// Función para actualizar el estado de autenticación en la interfaz
function actualizarEstadoAutenticacion() {
    const loginBtn = document.getElementById('loginBtn');
    const perfilBtn = document.getElementById('perfilBtn');
    
    if (isAuthenticated()) {
        if (loginBtn) loginBtn.classList.add('d-none');
        if (perfilBtn) perfilBtn.classList.remove('d-none');
    } else {
        if (loginBtn) loginBtn.classList.remove('d-none');
        if (perfilBtn) perfilBtn.classList.add('d-none');
    }
}

// Función para crear una tarjeta de producto
function crearProductoCard(producto, esOferta = false) {
    const card = document.createElement('div');
    card.className = 'col-md-4 mb-4';
    card.innerHTML = `
        <div class="card h-100 product-card">
            <div class="image-container">
                <img src="${producto.imagen}" class="card-img-top" alt="${producto.nombre}">
                <div class="image-overlay">
                    <div class="overlay-content">
                        <h3>${producto.nombre}</h3>
                        <p>${producto.descripcion}</p>
                    </div>
                </div>
            </div>
            <div class="card-body">
                <h5 class="card-title">${producto.nombre}</h5>
                <p class="card-text">${producto.descripcion}</p>
                <p class="card-text">
                    <small class="text-muted">
                        Plataforma: ${producto.plataforma}<br>
                        Stock disponible: ${producto.stock}
                    </small>
                </p>
                <div class="d-flex justify-content-between align-items-center">
                    <div>
                        ${producto.precioOriginal ? `
                            <span class="text-decoration-line-through text-muted">$${producto.precioOriginal.toFixed(2)}</span>
                            <span class="ms-2 text-danger">$${producto.precio.toFixed(2)}</span>
                            <span class="badge bg-danger ms-2">-$${(producto.precioOriginal - producto.precio).toFixed(2)}</span>
                        ` : `
                            <span class="h5 mb-0">$${producto.precio.toFixed(2)}</span>
                        `}
                    </div>
                    <button class="btn btn-primary" onclick="agregarAlCarrito(${producto.id})">
                        Agregar al Carrito
                    </button>
                </div>
            </div>
        </div>
    `;
    return card;
}

// Función para cargar productos destacados
function cargarProductosDestacados() {
    const container = document.getElementById('productos-container');
    if (!container) return;

    container.innerHTML = '';
    // Mostrar solo los primeros 3 productos como destacados
    productos.slice(0, 3).forEach(producto => {
        const card = crearProductoCard(producto);
        container.appendChild(card);
    });
}

// Función para cargar ofertas
function cargarOfertas() {
    const container = document.getElementById('ofertas-container');
    if (!container) return;

    const ofertas = [
        {
            id: 4,
            nombre: "Monster Hunter Wilds",
            precio: 50.00,
            precioOriginal: 60.00,
            imagen: "img/productos/monster hunter wilds.jpg",
            plataforma: "Steam",
            descripcion: "La nueva entrega de la saga Monster Hunter. Caza monstruos gigantes en un mundo dinámico y peligroso.",
            stock: 12,
            descuento: 10
        }
    ];

    container.innerHTML = '';
    ofertas.forEach(oferta => {
        const card = crearProductoCard(oferta, true);
        container.appendChild(card);
    });
}

// Función para cargar todos los productos
function cargarTodosLosProductos() {
    const container = document.getElementById('productos-container');
    if (!container) return;

    container.innerHTML = '';
    productos.forEach(producto => {
        const card = crearProductoCard(producto);
        container.appendChild(card);
    });
}

// Inicializar la página
document.addEventListener('DOMContentLoaded', () => {
    mostrarProductos();
    actualizarCarrito();
    cargarOfertas();
    cargarTodosLosProductos();
    actualizarEstadoAutenticacion();
    actualizarContadorCarrito();
    
    // Verificar si el usuario está autenticado
    const usuario = JSON.parse(sessionStorage.getItem('usuario'));
    if (usuario) {
        document.getElementById('btnLogin').innerHTML = `
            <i class="fas fa-user"></i> ${usuario.nombre}
        `;
    }
}); 