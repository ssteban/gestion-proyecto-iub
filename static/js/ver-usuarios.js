var ruta = 'http://127.0.0.1:5000';

document.getElementById("buscar-boton").addEventListener("click", function() {
    const nombre = document.getElementById("buscar-nombre").value;
    console.log(nombre)
    if (nombre) {
        obtenerUsuarios(1, nombre);
    } else {
        obtenerUsuarios();
    }
});

function mostrarProyectos(usuarios, pagina) {
    const listaUsuarios = document.getElementById("lista-proyectos");
    listaUsuarios.innerHTML = "";

    const usuariosPorPagina = 15;
    const inicio = (pagina - 1) * usuariosPorPagina;
    const fin = inicio + usuariosPorPagina;
    const usuariosPagina = usuarios.slice(inicio, fin);

    usuariosPagina.forEach(usuario => {
        const usuarioDiv = document.createElement("div");
        usuarioDiv.className = "proyecto";

        const id = document.createElement("h3");
        id.innerText = "ID: " + usuario.id;
        usuarioDiv.appendChild(id);

        const nombre = document.createElement("p");
        nombre.innerText = "Nombre: " + usuario.nombre;
        usuarioDiv.appendChild(nombre);

        const verButton = document.createElement("button");
        verButton.innerText = "Ver";
        verButton.className = "paginacion-btn";
        verButton.onclick = function() {
            mostrarDetallesUsuario(usuario.id);
        };
        usuarioDiv.appendChild(verButton);

        listaUsuarios.appendChild(usuarioDiv);
    });

    // Crear botones de paginación
    const paginacionDiv = document.getElementById("paginacion");
    paginacionDiv.innerHTML = "";

    if (pagina > 1) {
        const anteriorButton = document.createElement("button");
        anteriorButton.innerText = "Anterior";
        anteriorButton.className = "paginacion-btn";
        anteriorButton.onclick = function() {
            obtenerUsuarios(pagina - 1);
        };
        paginacionDiv.appendChild(anteriorButton);
    }

    if (fin < usuarios.length) {
        const siguienteButton = document.createElement("button");
        siguienteButton.innerText = "Siguiente";
        siguienteButton.className = "paginacion-btn";
        siguienteButton.onclick = function() {
            obtenerUsuarios(pagina + 1);
        };
        paginacionDiv.appendChild(siguienteButton);
    }
}

function mostrarDetallesUsuario(id) {
    fetch(ruta + '/usuario', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ id: id })
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Error al obtener los detalles del usuario');
        }
        return response.json();
    })
    .then(data => {
        const modal = document.getElementById("modal");
        const modalContent = document.getElementById("modal-content");
        modalContent.innerHTML = "";

        const form = document.createElement("form");
        form.id = "editar-usuario-form";

        const idInput = document.createElement("input");
        idInput.type = "hidden";
        idInput.name = "id";
        idInput.value = data.usuario.id;
        form.appendChild(idInput);

        const nombreLabel = document.createElement("label");
        nombreLabel.innerText = "Nombre: ";
        form.appendChild(nombreLabel);

        const nombreInput = document.createElement("input");
        nombreInput.type = "text";
        nombreInput.name = "nombre";
        nombreInput.value = data.usuario.nombre;
        form.appendChild(nombreInput);

        form.appendChild(document.createElement("br"));

        const correoLabel = document.createElement("label");
        correoLabel.innerText = "Correo: ";
        form.appendChild(correoLabel);

        const correoInput = document.createElement("input");
        correoInput.type = "email";
        correoInput.name = "correo";
        correoInput.value = data.usuario.correo;
        form.appendChild(correoInput);

        form.appendChild(document.createElement("br"));

        const programaLabel = document.createElement("label");
        programaLabel.innerText = "Programa: ";
        form.appendChild(programaLabel);

        const programaInput = document.createElement("input");
        programaInput.type = "text";
        programaInput.name = "programa";
        programaInput.value = data.usuario.programa;
        form.appendChild(programaInput);

        form.appendChild(document.createElement("br"));

        const usuarioLabel = document.createElement("label");
        usuarioLabel.innerText = "Usuario: ";
        form.appendChild(usuarioLabel);

        const usuarioInput = document.createElement("input");
        usuarioInput.type = "text";
        usuarioInput.name = "usuario";
        usuarioInput.value = data.usuario.usuario;
        form.appendChild(usuarioInput);

        form.appendChild(document.createElement("br"));

        const fechaLabel = document.createElement("label");
        fechaLabel.innerText = "Fecha de registro: ";
        form.appendChild(fechaLabel);

        const fechaInput = document.createElement("input");
        fechaInput.type = "text";
        fechaInput.name = "fecha";
        fechaInput.value = data.usuario.fecha;
        fechaInput.readOnly = true;
        form.appendChild(fechaInput);

        form.appendChild(document.createElement("br"));

        const actualizarButton = document.createElement("button");
        actualizarButton.type = "button";
        actualizarButton.innerText = "Actualizar";
        actualizarButton.className = "paginacion-btn";
        actualizarButton.onclick = function() {
            actualizarUsuario();
        };
        form.appendChild(actualizarButton);

        const cambiarContraseñaButton = document.createElement("button");
        cambiarContraseñaButton.type = "button";
        cambiarContraseñaButton.innerText = "Cambiar Contraseña";
        cambiarContraseñaButton.className = "paginacion-btn";
        cambiarContraseñaButton.onclick = function() {
            cambiarContraseña(data.usuario.correo);
        };
        form.appendChild(cambiarContraseñaButton);

        const cerrarButton = document.createElement("button");
        cerrarButton.type = "button";
        cerrarButton.innerText = "Cerrar";
        cerrarButton.className = "paginacion-btn";
        cerrarButton.onclick = function() {
            modal.style.display = "none";
        };
        form.appendChild(cerrarButton);

        modalContent.appendChild(form);
        modal.style.display = "block";

        window.scrollTo({ top: 0, behavior: 'smooth' });
    })
    .catch(error => {
        console.error('Error al obtener detalles del usuario:', error);
        alert('Hubo un problema al obtener los detalles del usuario.');
    });
}

function cambiarContraseña(correo) {
    fetch(ruta + '/send-mail', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ correo: correo })
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Error al enviar el correo de cambio de contraseña');
        }
        return response.json();
    })
    .then(data => {
        if (data.success) {
            alert('Correo de cambio de contraseña enviado exitosamente');
        } else {
            alert('Error al enviar el correo de cambio de contraseña: ' + data.message);
        }
    })
    .catch(error => {
        console.error('Error al enviar el correo de cambio de contraseña:', error);
        alert('Hubo un problema al enviar el correo de cambio de contraseña.');
    });
}

function actualizarUsuario() {
    const form = document.getElementById("editar-usuario-form");
    const formData = new FormData(form);
    const usuarioData = {};

    formData.forEach((value, key) => {
        usuarioData[key] = value;
    });

    fetch(ruta + '/actualizar_usuario', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(usuarioData)
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Error al actualizar el usuario');
        }
        return response.json();
    })
    .then(data => {
        if (data.success) {
            alert('Usuario actualizado exitosamente');
            document.getElementById("modal").style.display = "none";
            obtenerUsuarios();
        } else {
            alert('Error al actualizar usuario: ' + data.message);
        }
    })
    .catch(error => {
        console.error('Error al actualizar usuario:', error);
        alert('Hubo un problema al actualizar el usuario.');
    });
}

function obtenerUsuarios(pagina = 1, nombre = "") {
    fetch(ruta + '/ver_usuarios', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ nombre: nombre })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            mostrarProyectos(data.usuarios, pagina);
            window.scrollTo({ top: 0, behavior: 'smooth' });
        } else {
            alert('Error al obtener usuarios: ' + data.message);
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('Hubo un problema al obtener los usuarios.');
    });
}

// Llamada inicial para obtener y mostrar usuarios
obtenerUsuarios();
