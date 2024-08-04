(function () {
    var ruta = 'http://127.0.0.1:5000';

    var loadingModal = document.getElementById('loadingModal');
    loadingModal.style.display = 'block';
    obtener_informacion();

    function obtener_informacion() {
        const correoUsuario = JSON.parse(localStorage.getItem('loggedInUser'));
        console.log('Correo Usuario:', correoUsuario.user); // Verificar el valor del correo
        fetch(ruta + '/datos-u', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ correo: correoUsuario.user })
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Error al obtener los datos del estudiante');
            }
            return response.json();
        })
        .then(data => {
            loadingModal.style.display = 'none';
            console.log('Datos recibidos:', data); // Verificar los datos recibidos
            document.getElementById('nombre-completo').value = data.datos.nombre;
            document.getElementById('correo').value = data.datos.correo;
            document.getElementById('programa').value = data.datos.programa;
            document.getElementById('nombre-usuario').value = data.datos.usuario || ''; // Verificar si este campo existe en los datos
            document.getElementById('fecha').value = data.datos.fecha;
    
            // Actualizar la imagen de perfil
            if (data.datos.foto) {
                document.getElementById('profileImg').src = 'data:image/png;base64,' + data.datos.foto;
            }
        })
        .catch(error => {
            loadingModal.style.display = 'none';
            console.error('Error al obtener los datos del estudiante:', error);
        });
    }
    // Mostrar el modal de Actualizar Contraseña al hacer clic en el botón
    document.getElementById('updatePasswordBtn').addEventListener('click', function () {
        var updatePasswordModal = document.getElementById('updatePasswordModal');
        updatePasswordModal.style.display = 'block';
    });


    // Cerrar el modal si se hace clic fuera del contenido del modal
    window.onclick = function (event) {
        if (event.target.classList.contains('modal')) {
            event.target.style.display = 'none';
        }
    };

    document.getElementById('updatePasswordForm').addEventListener('submit', function (event) {
        event.preventDefault();

        var oldPassword = document.getElementById('oldPassword').value;
        var newPassword = document.getElementById('newPassword').value;
        var confirmNewPassword = document.getElementById('confirmNewPassword').value;
        var correo = JSON.parse(localStorage.getItem('loggedInUser'));

        if (newPassword !== confirmNewPassword) {
            alert('Las nuevas contraseñas no coinciden.');
            return;
        }

        if (!contra(newPassword)) {
            return;
        }
        console.log(correo, oldPassword, newPassword)
        loadingModal.style.display = 'block';

        fetch(ruta + '/actualizar_contra_p', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ correo: correo.user, oldPassword: oldPassword, newPassword: newPassword })
        })
            .then(response => response.json())
            .then(data => {
                loadingModal.style.display = 'none';

                if (data.success) {
                    alert('Contraseña actualizada con éxito.');
                    document.getElementById('updatePasswordModal').style.display = 'none';
                } else {
                    alert('Error al actualizar la contraseña: ' + data.message);
                }
            })
            .catch(error => {
                loadingModal.style.display = 'none';
                console.error('Error:', error);
                alert('Hubo un problema al actualizar la contraseña.');
            });
    });

    function contra(pass) {
        if (pass.length < 6 || pass.length > 12) {
            alert('La contraseña debe tener entre 6 y 12 caracteres');
            return false;
        } else {
            return true;
        }
    }


})();

// Mostrar el modal de Cambiar Foto de Perfil al hacer clic en la imagen de perfil
function mostrarM() {
    var changePhotoModal = document.getElementById('changePhotoModal');
    changePhotoModal.style.display = 'block';
}

function actualizar() {
    const ruta = 'http://127.0.0.1:5000';
    const usuario = document.getElementById('nombre-usuario').value;
    console.log(usuario)
    const correoUsuario = JSON.parse(localStorage.getItem('loggedInUser'));
    fetch(ruta + '/actualizar', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ user: usuario, correo: correoUsuario.user })
    })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                alert(data.message);
            } else {
                alert('Error al actualizar los datos: ' + data.message);
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('Hubo un problema al actualizar los datos.');
        });
}


function subirfoto() {
    var fileInput = document.getElementById('newProfilePhoto');
    var file = fileInput.files[0];
    if (file) {
        var reader = new FileReader();
        reader.onloadend = function () {
            var img = new Image();
            img.src = reader.result;
            img.onload = function () {
                var canvas = document.createElement('canvas');
                var ctx = canvas.getContext('2d');

                // Establecer el tamaño máximo deseado
                var MAX_WIDTH = 200;
                var MAX_HEIGHT = 200;
                var width = img.width;
                var height = img.height;

                if (width > height) {
                    if (width > MAX_WIDTH) {
                        height *= MAX_WIDTH / width;
                        width = MAX_WIDTH;
                    }
                } else {
                    if (height > MAX_HEIGHT) {
                        width *= MAX_HEIGHT / height;
                        height = MAX_HEIGHT;
                    }
                }
                canvas.width = width;
                canvas.height = height;

                ctx.drawImage(img, 0, 0, width, height);

                var base64String = canvas.toDataURL('image/png').replace('data:image/png;base64,', '');
                
                // Mostrar la imagen redimensionada en el perfil inmediatamente
                document.getElementById('profileImg').src = 'data:image/png;base64,' + base64String;

                // Enviar la imagen redimensionada al servidor
                const correoUsuario = JSON.parse(localStorage.getItem('loggedInUser'));
                fetch(ruta + '/fotoP', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({
                        correo: correoUsuario.user,
                        foto: base64String
                    })
                })
                .then(response => response.json())
                //cerrar modal 
                .then(data => {
                    if (data.success) {
                        var modal = document.getElementById('changePhotoModal');
                        modal.style.display = 'none';
                        alert(data.message);
                    } else {
                        console.log('Error al subir la foto de perfil: ' + data.message);
                    }
                })
                .catch(error => {
                    var modal = document.getElementById('changePhotoModal');
                    modal.style.display = 'none';
                    console.error('Error:', error);
                    console.log('Hubo un problema al subir la foto de perfil.');
                });
            };
        };
        reader.readAsDataURL(file);
    }
}


