// Verificar autenticación
document.addEventListener('DOMContentLoaded', () => {
    if (!isAuthenticated()) {
        window.location.href = 'login.html';
        return;
    }

    // Cargar datos del usuario
    cargarDatosUsuario();
    cargarTarjetas();
    cargarHistorialCompras();

    // Event listeners para formularios
    document.getElementById('datos-personales-form').addEventListener('submit', actualizarDatosPersonales);
    document.getElementById('tarjeta-form').addEventListener('submit', agregarTarjeta);
});

// Cargar datos del usuario
function cargarDatosUsuario() {
    const usuario = getUsuarioActual();
    if (usuario) {
        document.getElementById('nombre').value = usuario.nombre || '';
        document.getElementById('apellido').value = usuario.apellido || '';
        document.getElementById('email').value = usuario.email || '';
        document.getElementById('telefono').value = usuario.telefono || '';
    }
}

// Actualizar datos personales
function actualizarDatosPersonales(e) {
    e.preventDefault();
    
    const usuario = getUsuarioActual();
    if (!usuario) return;

    const nuevosDatos = {
        nombre: document.getElementById('nombre').value,
        apellido: document.getElementById('apellido').value,
        email: document.getElementById('email').value,
        telefono: document.getElementById('telefono').value
    };

    // Actualizar contraseña si se proporciona
    const password = document.getElementById('password').value;
    const confirmPassword = document.getElementById('confirm-password').value;
    
    if (password && password === confirmPassword) {
        nuevosDatos.password = password;
    }

    // Actualizar usuario en localStorage
    const usuarios = JSON.parse(localStorage.getItem('usuarios') || '[]');
    const index = usuarios.findIndex(u => u.email === usuario.email);
    if (index !== -1) {
        usuarios[index] = { ...usuarios[index], ...nuevosDatos };
        localStorage.setItem('usuarios', JSON.stringify(usuarios));
        localStorage.setItem('usuarioActual', JSON.stringify(usuarios[index]));
    }

    alert('Datos actualizados correctamente');
}

// Cargar tarjetas guardadas
function cargarTarjetas() {
    const usuario = getUsuarioActual();
    if (!usuario || !usuario.tarjetas) return;

    const container = document.getElementById('tarjetas-container');
    container.innerHTML = '';

    usuario.tarjetas.forEach((tarjeta, index) => {
        const card = document.createElement('div');
        card.className = 'card mb-3';
        card.innerHTML = `
            <div class="card-body">
                <h5 class="card-title">Tarjeta ${index + 1}</h5>
                <p class="card-text">
                    <strong>Número:</strong> ${tarjeta.numero.replace(/(\d{4})/g, '$1 ').replace(/(\d{4} ){3}/, '**** **** **** ')}<br>
                    <strong>Expira:</strong> ${tarjeta.fechaExpiracion}<br>
                    <strong>Nombre:</strong> ${tarjeta.nombre}
                </p>
                <button class="btn btn-danger btn-sm" onclick="eliminarTarjeta(${index})">Eliminar</button>
            </div>
        `;
        container.appendChild(card);
    });
}

// Agregar nueva tarjeta
function agregarTarjeta(e) {
    e.preventDefault();
    
    const usuario = getUsuarioActual();
    if (!usuario) return;

    const nuevaTarjeta = {
        numero: document.getElementById('numero-tarjeta').value,
        fechaExpiracion: document.getElementById('fecha-expiracion').value,
        cvv: document.getElementById('cvv').value,
        nombre: document.getElementById('nombre-tarjeta').value
    };

    // Inicializar array de tarjetas si no existe
    if (!usuario.tarjetas) {
        usuario.tarjetas = [];
    }

    // Agregar nueva tarjeta
    usuario.tarjetas.push(nuevaTarjeta);

    // Actualizar usuario en localStorage
    const usuarios = JSON.parse(localStorage.getItem('usuarios') || '[]');
    const index = usuarios.findIndex(u => u.email === usuario.email);
    if (index !== -1) {
        usuarios[index] = usuario;
        localStorage.setItem('usuarios', JSON.stringify(usuarios));
        localStorage.setItem('usuarioActual', JSON.stringify(usuario));
    }

    // Cerrar modal y recargar tarjetas
    const modal = bootstrap.Modal.getInstance(document.getElementById('agregarTarjetaModal'));
    modal.hide();
    cargarTarjetas();
    e.target.reset();
}

// Eliminar tarjeta
function eliminarTarjeta(index) {
    if (!confirm('¿Estás seguro de que deseas eliminar esta tarjeta?')) return;

    const usuario = getUsuarioActual();
    if (!usuario || !usuario.tarjetas) return;

    usuario.tarjetas.splice(index, 1);

    // Actualizar usuario en localStorage
    const usuarios = JSON.parse(localStorage.getItem('usuarios') || '[]');
    const userIndex = usuarios.findIndex(u => u.email === usuario.email);
    if (userIndex !== -1) {
        usuarios[userIndex] = usuario;
        localStorage.setItem('usuarios', JSON.stringify(usuarios));
        localStorage.setItem('usuarioActual', JSON.stringify(usuario));
    }

    cargarTarjetas();
}

// Cargar historial de compras
function cargarHistorialCompras() {
    const usuario = getUsuarioActual();
    if (!usuario || !usuario.compras) return;

    const container = document.getElementById('historial-container');
    container.innerHTML = '';

    usuario.compras.forEach(compra => {
        const card = document.createElement('div');
        card.className = 'card mb-3';
        card.innerHTML = `
            <div class="card-body">
                <h5 class="card-title">Compra #${compra.id}</h5>
                <p class="card-text">
                    <strong>Fecha:</strong> ${new Date(compra.fecha).toLocaleDateString()}<br>
                    <strong>Total:</strong> $${compra.total.toFixed(2)}<br>
                    <strong>Estado:</strong> ${compra.estado}
                </p>
                <button class="btn btn-primary btn-sm" onclick="verDetallesCompra('${compra.id}')">Ver Detalles</button>
            </div>
        `;
        container.appendChild(card);
    });
}

// Ver detalles de compra
function verDetallesCompra(compraId) {
    const usuario = getUsuarioActual();
    if (!usuario || !usuario.compras) return;

    const compra = usuario.compras.find(c => c.id === compraId);
    if (!compra) return;

    let detalles = 'Detalles de la Compra:\n\n';
    compra.productos.forEach(producto => {
        detalles += `${producto.nombre} - $${producto.precio.toFixed(2)}\n`;
    });
    detalles += `\nTotal: $${compra.total.toFixed(2)}`;

    alert(detalles);
} 