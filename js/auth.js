// Datos de ejemplo (en un caso real, estos vendrían de una base de datos)
const usuarios = [
    {
        id: 1,
        nombre: "Admin",
        email: "admin@YZtore.com",
        password: "admin123",
        rol: "admin"
    },
    {
        id: 2,
        nombre: "Usuario Ejemplo",
        email: "usuario@ejemplo.com",
        password: "usuario123",
        rol: "cliente"
    }
];

// Función para manejar el inicio de sesión
document.getElementById('loginForm').addEventListener('submit', function(e) {
    e.preventDefault();
    
    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;
    
    const usuario = usuarios.find(u => u.email === email && u.password === password);
    
    if (usuario) {
        // Guardar información del usuario en sessionStorage
        sessionStorage.setItem('usuario', JSON.stringify({
            id: usuario.id,
            nombre: usuario.nombre,
            email: usuario.email,
            rol: usuario.rol
        }));
        
        // Redirigir según el rol
        if (usuario.rol === 'admin') {
            window.location.href = 'admin/panel.html';
        } else {
            window.location.href = 'index.html';
        }
    } else {
        alert('Credenciales inválidas. Por favor, intente nuevamente.');
    }
});

// Función para manejar el registro
document.getElementById('registroForm').addEventListener('submit', function(e) {
    e.preventDefault();
    
    const nombre = document.getElementById('nombre').value;
    const email = document.getElementById('emailRegistro').value;
    const password = document.getElementById('passwordRegistro').value;
    const confirmPassword = document.getElementById('confirmPassword').value;
    
    // Validar que las contraseñas coincidan
    if (password !== confirmPassword) {
        alert('Las contraseñas no coinciden.');
        return;
    }
    
    // Validar que el email no exista
    if (usuarios.some(u => u.email === email)) {
        alert('El correo electrónico ya está registrado.');
        return;
    }
    
    // Crear nuevo usuario
    const nuevoUsuario = {
        id: usuarios.length + 1,
        nombre: nombre,
        email: email,
        password: password,
        rol: 'cliente'
    };
    
    usuarios.push(nuevoUsuario);
    
    // Cerrar modal y mostrar mensaje de éxito
    const modal = bootstrap.Modal.getInstance(document.getElementById('registroModal'));
    modal.hide();
    alert('Registro exitoso. Por favor, inicie sesión.');
    
    // Limpiar formulario
    this.reset();
});

// Función para verificar si el usuario está autenticado
function verificarAutenticacion() {
    const usuario = JSON.parse(sessionStorage.getItem('usuario'));
    if (!usuario) {
        window.location.href = 'login.html';
    }
    return usuario;
}

// Verificar autenticación en páginas protegidas
if (window.location.pathname.includes('admin/')) {
    const usuario = verificarAutenticacion();
    if (usuario && usuario.rol !== 'admin') {
        window.location.href = '../index.html';
    }
} 