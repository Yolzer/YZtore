// Datos de ejemplo (en un caso real, estos vendrían de una base de datos)
let productos = [
    {
        id: 1,
        nombre: "The Witcher 3: Wild Hunt",
        plataforma: "Steam",
        precio: 29.99,
        stock: 10,
        descripcion: "Juego de rol de mundo abierto galardonado"
    },
    {
        id: 2,
        nombre: "Red Dead Redemption 2",
        plataforma: "Epic Games",
        precio: 59.99,
        stock: 5,
        descripcion: "Aventura del Salvaje Oeste"
    }
];

let inventario = [
    {
        id: "KEY-001",
        producto: "The Witcher 3: Wild Hunt",
        estado: "Disponible",
        fechaAdquisicion: "2024-03-15"
    },
    {
        id: "KEY-002",
        producto: "Red Dead Redemption 2",
        estado: "Vendido",
        fechaAdquisicion: "2024-03-14"
    }
];

let ventas = [
    {
        id: "V-001",
        cliente: "usuario@ejemplo.com",
        producto: "Red Dead Redemption 2",
        fecha: "2024-03-14",
        total: 59.99,
        estado: "Completada"
    }
];

// Función para cargar productos en la tabla
function cargarProductos() {
    const tbody = document.getElementById('productosTable');
    tbody.innerHTML = '';
    
    productos.forEach(producto => {
        const tr = document.createElement('tr');
        tr.innerHTML = `
            <td>${producto.id}</td>
            <td>${producto.nombre}</td>
            <td>${producto.plataforma}</td>
            <td>$${producto.precio}</td>
            <td>${producto.stock}</td>
            <td>
                <button class="btn btn-sm btn-primary" onclick="editarProducto(${producto.id})">
                    <i class="fas fa-edit"></i>
                </button>
                <button class="btn btn-sm btn-danger" onclick="eliminarProducto(${producto.id})">
                    <i class="fas fa-trash"></i>
                </button>
            </td>
        `;
        tbody.appendChild(tr);
    });
}

// Función para cargar inventario
function cargarInventario() {
    const tbody = document.getElementById('inventarioTable');
    tbody.innerHTML = '';
    
    inventario.forEach(item => {
        const tr = document.createElement('tr');
        tr.innerHTML = `
            <td>${item.id}</td>
            <td>${item.producto}</td>
            <td>${item.estado}</td>
            <td>${item.fechaAdquisicion}</td>
            <td>
                <button class="btn btn-sm btn-info" onclick="verDetallesKey('${item.id}')">
                    <i class="fas fa-eye"></i>
                </button>
            </td>
        `;
        tbody.appendChild(tr);
    });
}

// Función para cargar ventas
function cargarVentas() {
    const tbody = document.getElementById('ventasTable');
    tbody.innerHTML = '';
    
    ventas.forEach(venta => {
        const tr = document.createElement('tr');
        tr.innerHTML = `
            <td>${venta.id}</td>
            <td>${venta.cliente}</td>
            <td>${venta.producto}</td>
            <td>${venta.fecha}</td>
            <td>$${venta.total}</td>
            <td>${venta.estado}</td>
        `;
        tbody.appendChild(tr);
    });
}

// Función para agregar nuevo producto
document.getElementById('productoForm').addEventListener('submit', function(e) {
    e.preventDefault();
    
    const nuevoProducto = {
        id: productos.length + 1,
        nombre: document.getElementById('nombreProducto').value,
        plataforma: document.getElementById('plataforma').value,
        precio: parseFloat(document.getElementById('precio').value),
        stock: 0,
        descripcion: document.getElementById('descripcion').value
    };
    
    productos.push(nuevoProducto);
    cargarProductos();
    
    // Cerrar modal y limpiar formulario
    const modal = bootstrap.Modal.getInstance(document.getElementById('productoModal'));
    modal.hide();
    this.reset();
});

// Función para editar producto
function editarProducto(id) {
    const producto = productos.find(p => p.id === id);
    if (producto) {
        document.getElementById('nombreProducto').value = producto.nombre;
        document.getElementById('plataforma').value = producto.plataforma;
        document.getElementById('precio').value = producto.precio;
        document.getElementById('descripcion').value = producto.descripcion;
        
        const modal = new bootstrap.Modal(document.getElementById('productoModal'));
        modal.show();
    }
}

// Función para eliminar producto
function eliminarProducto(id) {
    if (confirm('¿Estás seguro de que deseas eliminar este producto?')) {
        productos = productos.filter(p => p.id !== id);
        cargarProductos();
    }
}

// Función para ver detalles de una key
function verDetallesKey(id) {
    const key = inventario.find(k => k.id === id);
    if (key) {
        alert(`Detalles de la Key:\nID: ${key.id}\nProducto: ${key.producto}\nEstado: ${key.estado}\nFecha: ${key.fechaAdquisicion}`);
    }
}

// Función para cerrar sesión
function cerrarSesion() {
    // Aquí se implementaría la lógica de cierre de sesión
    window.location.href = '../login.html';
}

// Inicializar la página
document.addEventListener('DOMContentLoaded', () => {
    cargarProductos();
    cargarInventario();
    cargarVentas();
}); 