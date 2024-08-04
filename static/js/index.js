function contra(pass) {
    if (pass.length < 6 || pass.length > 12) {
        alert('La contraseña debe tener al menos entre 6 y 12 caracteres');
        return false;
    } else {
        return true;
    } 
}

var ruta = 'http://127.0.0.1:5000';

document.getElementById('loginForm').addEventListener('submit', function (event) {
    event.preventDefault();

    var email = document.getElementById('email').value;
    var password = document.getElementById('password').value;
    var loadingModal = document.getElementById('loadingModal');

    if (email.includes("@unibarranquilla.edu.co")) {
        if (contra(password)) {

            loadingModal.style.display = 'block';

            fetch(ruta + '/login-u', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ email: email, password: password })
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    loadingModal.style.display = 'none';
                    if (data.role === 'estudiante') {
                        localStorage.setItem('loggedInUser', JSON.stringify({ user: email}));
                        window.location.href = 'templates/usuario/inicio-u.html';
                    } else if (data.role === 'administrador') {
                        alert('Bienvenido admin')
                        localStorage.setItem('loggedInUser', JSON.stringify({ user: email}));
                        window.location.href = 'templates/admin/inicio-u.html';
                    } else {
                        alert('Rol de usuario desconocido.');
                    }
                } else {
                    loadingModal.style.display = 'none';
                    alert('Error en el inicio de sesión: ' + data.message);
                }
            })
            .catch(error => {
                loadingModal.style.display = 'none';
                console.error('Error:', error);
                alert('Hubo un problema con el inicio de sesión.');
            });
        }
    } else {
        alert("Ingrese un correo institucional válido.");
    }
});
