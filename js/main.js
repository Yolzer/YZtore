// Datos de ejemplo de productos
const productos = [
    {
        id: 1,
        nombre: "The Witcher 3: Wild Hunt",
        precio: 29.99,
        imagen: "https://via.placeholder.com/300x200",
        plataforma: "Steam",
        descripcion: "Juego de rol de mundo abierto galardonado"
    },
    {
        id: 2,
        nombre: "Red Dead Redemption 2",
        precio: 59.99,
        imagen: "https://via.placeholder.com/300x200",
        plataforma: "Epic Games",
        descripcion: "Aventura del Salvaje Oeste"
    },
    {
        id: 3,
        nombre: "Cyberpunk 2077",
        precio: 39.99,
        imagen: "https://via.placeholder.com/300x200",
        plataforma: "GOG",
        descripcion: "RPG de acción y aventura futurista"
    }
];

// Función para mostrar productos en la página
function mostrarProductos() {
    const contenedor = document.getElementById('featured-products');
    
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
                            <button class="btn btn-primary" onclick="agregarAlCarrito(${producto.id})">
                                <i class="fas fa-shopping-cart"></i> Comprar
                            </button>
                        </div>
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
    if (producto) {
        // Aquí se implementaría la lógica del carrito
        alert(`¡${producto.nombre} agregado al carrito!`);
    }
}

// Inicializar la página
document.addEventListener('DOMContentLoaded', () => {
    mostrarProductos();
    
    // Inicializar tooltips de Bootstrap
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
}); 