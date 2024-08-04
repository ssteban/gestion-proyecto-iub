function inicializarVerProyectos() {
    var ruta = 'http://127.0.0.1:5000';
    const proyectosPorPagina = 15;
    let paginaActual = 1;

    function obtenerProyectos(pagina = 1) {
        const correoUsuario = JSON.parse(localStorage.getItem('loggedInUser'));
        fetch(ruta + '/mis-proyectos', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ correo: correoUsuario.user }) 
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                paginaActual = pagina;
                mostrarProyectos(data.proyectos, pagina);
                // Desplazarse hacia la parte superior de la página
                window.scrollTo({ top: 0, behavior: 'smooth' });
            } else {
                alert('Error al obtener proyectos: ' + data.message);
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('Hubo un problema al obtener los proyectos.');
        });
    }

    function mostrarProyectos(proyectos, pagina) {
        const listaProyectos = document.getElementById("lista-proyectos");
        listaProyectos.innerHTML = "";
    
        const inicio = (pagina - 1) * proyectosPorPagina;
        const fin = inicio + proyectosPorPagina;
        const proyectosPagina = proyectos.slice(inicio, fin);
    
        proyectosPagina.forEach(proyecto => {
            const proyectoDiv = document.createElement("div");
            proyectoDiv.className = "proyecto";
    
            const titulo = document.createElement("h3");
            titulo.innerText = proyecto.titulo;
            proyectoDiv.appendChild(titulo);
    
            const resumen = document.createElement("p");
            resumen.innerText = proyecto.resumen;
            proyectoDiv.appendChild(resumen);
    
            const botonesDiv = document.createElement("div");
            botonesDiv.className = "botones";
    
            const verButton = document.createElement("button");
            verButton.innerText = "Ver";
            verButton.className = "paginacion-btn";
            verButton.onclick = function() {
                mostrarDetallesProyecto(proyecto.id);
            };
            botonesDiv.appendChild(verButton);
    
            proyectoDiv.appendChild(botonesDiv);
            listaProyectos.appendChild(proyectoDiv);
        });

        // Crear botones de paginación
        const paginacionDiv = document.getElementById("paginacion");
        paginacionDiv.innerHTML = "";
    
        if (pagina > 1) {
            const anteriorButton = document.createElement("button");
            anteriorButton.innerText = "Anterior";
            anteriorButton.className = "paginacion-btn";
            anteriorButton.onclick = function() {
                obtenerProyectos(pagina - 1);
            };
            paginacionDiv.appendChild(anteriorButton);
        }
    
        if (fin < proyectos.length) {
            const siguienteButton = document.createElement("button");
            siguienteButton.innerText = "Siguiente";
            siguienteButton.className = "paginacion-btn";
            siguienteButton.onclick = function() {
                obtenerProyectos(pagina + 1);
            };
            paginacionDiv.appendChild(siguienteButton);
        }
    }

    function mostrarDetallesProyecto(id) {
        fetch(ruta + '/proyecto', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ id: id })  // Enviar id como parte del cuerpo JSON
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Error al obtener los detalles del proyecto');
            }
            return response.json();
        })
        .then(data => {
            if (!data.success) {
                throw new Error(data.message || 'Datos del proyecto no disponibles');
            }
    
            const modal = document.getElementById("modal");
            const modalContent = document.getElementById("modal-content");
            modalContent.innerHTML = "";
    
            const fields = [
                { label: "Título", value: data.proyecto.titulo },
                { label: "Resumen", value: data.proyecto.resumen },
                { label: "Facultad", value: data.proyecto.facultad },
                { label: "Programa", value: data.proyecto.programa },
                { label: "Tipo De Proyecto", value: data.proyecto.tipo },
                { label: "Palabras Clave", value: data.proyecto.palabras_clave },
                { label: "Estado Del Proyecto", value: data.proyecto.estado },
                { label: "Estudiantes", value: data.proyecto.estudiantes },
                { label: "Docente Encargado", value: data.proyecto.docente },
                { label: "Registrado Por", value: data.proyecto.registrado },
                { label: "Fecha De Registro", value: data.proyecto.fecha }
            ];
    
            fields.forEach(field => {
                const label = document.createElement("label");
                label.innerText = `${field.label}:`;
                const input = document.createElement("input");
                input.value = field.value;
                input.readOnly = true;
                modalContent.appendChild(label);
                modalContent.appendChild(input);
                modalContent.appendChild(document.createElement("br"));
            });
    
            // Convertir base64 a Blob y crear un enlace para el documento
            if (data.doc && data.doc.archivo) {
                const byteCharacters = atob(data.doc.archivo);
                const byteNumbers = new Array(byteCharacters.length);
                for (let i = 0; i < byteCharacters.length; i++) {
                    byteNumbers[i] = byteCharacters.charCodeAt(i);
                }
                const byteArray = new Uint8Array(byteNumbers);
                const blob = new Blob([byteArray], { type: 'application/pdf' }); // Cambia el tipo MIME si es necesario
    
                const downloadLink = document.createElement("a");
                downloadLink.href = URL.createObjectURL(blob);
                downloadLink.download = data.doc.titulo;
                downloadLink.innerText = "Ver Documento";
                downloadLink.className = "ver-documento-btn";
                downloadLink.style.display = "inline-block";
                downloadLink.target = "_blank"; // Abre en una nueva pestaña
    
                modalContent.appendChild(downloadLink);
                modalContent.appendChild(document.createElement("br"));
            }
    
            // Botón para subir documento
            const uploadButton = document.createElement("button");
            uploadButton.innerText = "Subir Documento";
            uploadButton.className = "upload-btn";
            uploadButton.onclick = function() {
                mostrarSubidaDocumento(id);
            };
            modalContent.appendChild(uploadButton);
    
            // Botón para cerrar el modal
            const cerrarButton = document.createElement("button");
            cerrarButton.innerText = "Cerrar";
            cerrarButton.className = "paginacion-btn";
            cerrarButton.onclick = function() {
                modal.style.display = "none";
            };
            modalContent.appendChild(cerrarButton);
    
            // Mostrar el modal
            modal.style.display = "block";
    
            // Desplazarse hacia la parte superior de la página
            window.scrollTo({ top: 0, behavior: 'smooth' });
        })
        .catch(error => {
            console.error('Error al obtener detalles del proyecto:', error.message);
            alert('Hubo un problema al obtener los detalles del proyecto: ' + error.message);
        });
    }    

    function mostrarSubidaDocumento(proyectoId) {
        const modalContent = document.getElementById("modal-content");

        // Crear un contenedor para el formulario de subida de documento
        const uploadDiv = document.createElement("div");
        uploadDiv.id = "upload-document";
        uploadDiv.innerHTML = `
            <label for="file-input">Seleccionar archivo:</label>
            <input type="file" id="file-input" />
            <button id="upload-button">Subir</button>
        `;
        modalContent.appendChild(uploadDiv);

        document.getElementById("upload-button").onclick = function() {
            subirDocumento(proyectoId);
        };
    }

    function subirDocumento(proyectoId) {
        const fileInput = document.getElementById("file-input");
        const file = fileInput.files[0];

        if (file) {
            const reader = new FileReader();
            reader.onload = function(e) {
                const base64File = e.target.result.split(',')[1];
                enviarDocumentoAlServidor(proyectoId, base64File, file.name);
            };
            reader.readAsDataURL(file);
        } else {
            alert("Por favor, selecciona un archivo.");
        }
    }

    function enviarDocumentoAlServidor(proyectoId, base64File, fileName) {
        fetch(ruta + '/obtenerdocumento', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                proyecto_id: proyectoId,
                archivo: base64File,
                nombre_archivo: fileName
            })
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                alert("Documento subido exitosamente.");
                document.getElementById("upload-document").style.display = "none";
            } else {
                alert("Error al subir el documento: " + data.message);
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('Hubo un problema al subir el documento.');
        });
    }

    // Llamada inicial para obtener y mostrar proyectos
    obtenerProyectos();
}

inicializarVerProyectos();
