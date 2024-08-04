(function () {
    var ruta = 'http://127.0.0.1:5000';


    const proyectosPorPagina = 15;
    let paginaActual = 1;
    let listaProyectos = []; // Almacena todos los proyectos

    function mostrarProyectos(proyectos, pagina) {
        const listaProyectosDiv = document.getElementById("lista-proyectos");
        listaProyectosDiv.innerHTML = "";

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

            const verButton = document.createElement("button");
            verButton.innerText = "Ver";
            verButton.className = "paginacion-btn";
            verButton.onclick = function () {
                mostrarDetallesProyecto(proyecto.id);
            };
            proyectoDiv.appendChild(verButton);

            listaProyectosDiv.appendChild(proyectoDiv);
        });

        const paginacionDiv = document.getElementById("paginacion");
        paginacionDiv.innerHTML = "";

        if (pagina > 1) {
            const anteriorButton = document.createElement("button");
            anteriorButton.innerText = "Anterior";
            anteriorButton.className = "paginacion-btn";
            anteriorButton.onclick = function () {
                mostrarProyectos(listaProyectos, pagina - 1);
            };
            paginacionDiv.appendChild(anteriorButton);
        }

        if (fin < proyectos.length) {
            const siguienteButton = document.createElement("button");
            siguienteButton.innerText = "Siguiente";
            siguienteButton.className = "paginacion-btn";
            siguienteButton.onclick = function () {
                mostrarProyectos(listaProyectos, pagina + 1);
            };
            paginacionDiv.appendChild(siguienteButton);
        }
    }

    function obtenerProyectos(pagina = 1) {
        fetch(ruta + '/ver_proyectos', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            }
        })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    paginaActual = pagina;
                    listaProyectos = data.proyectos.sort((a, b) => b.id - a.id);
                    mostrarProyectos(listaProyectos, pagina);
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

    window.buscar = function () {
        const searchTerm = document.getElementById("nombre-proyecto").value.toLowerCase();
        const proyectosFiltrados = listaProyectos.filter(proyecto =>
            proyecto.titulo.toLowerCase().includes(searchTerm)
        );
        document.getElementById("nombre-proyecto").value = "";
        mostrarProyectos(proyectosFiltrados, 1);
    };

    function mostrarDetallesProyecto(id) {
        fetch(ruta + '/proyecto', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ id: id })
        })
            .then(response => {
                if (!response.ok) {
                    throw new Error('Error al obtener los detalles del proyecto');
                }
                return response.json();
            })
            .then(data => {
                const modal = document.getElementById("modal");
                const modalContent = document.getElementById("modal-content");
                modalContent.innerHTML = "";

                const titulo = document.createElement("h2");
                titulo.innerText = data.proyecto.titulo;
                modalContent.appendChild(titulo);

                const resumen = document.createElement("p");
                resumen.innerText = data.proyecto.resumen;
                modalContent.appendChild(resumen);

                const facultad = document.createElement("p");
                facultad.innerText = "Facultad: " + data.proyecto.facultad;
                modalContent.appendChild(facultad);

                const programa = document.createElement("p");
                programa.innerText = "Programa: " + data.proyecto.programa;
                modalContent.appendChild(programa);

                const tipo = document.createElement("p");
                tipo.innerText = "Tipo de Proyecto: " + data.proyecto.tipo;
                modalContent.appendChild(tipo);

                const palabrasClave = document.createElement("p");
                palabrasClave.innerText = "Palabras Clave: " + data.proyecto.palabras_clave;
                modalContent.appendChild(palabrasClave);

                const estado = document.createElement("p");
                estado.innerText = "Estado del Proyecto: " + data.proyecto.estado;
                modalContent.appendChild(estado);

                const estudiantes = document.createElement("p");
                estudiantes.innerText = "Estudiantes: " + data.proyecto.estudiantes;
                modalContent.appendChild(estudiantes);

                const docente = document.createElement("p");
                docente.innerText = "Docente Encargado: " + data.proyecto.docente;
                modalContent.appendChild(docente);

                const registrado = document.createElement("p");
                registrado.innerText = "Registrado por: " + data.proyecto.registrado;
                modalContent.appendChild(registrado);

                const fecha = document.createElement("p");
                fecha.innerText = "Fecha Registro: " + data.proyecto.fecha;
                modalContent.appendChild(fecha);

                if (data.doc && data.doc.archivo) {
                    const byteCharacters = atob(data.doc.archivo);
                    const byteNumbers = new Array(byteCharacters.length);
                    for (let i = 0; i < byteCharacters.length; i++) {
                        byteNumbers[i] = byteCharacters.charCodeAt(i);
                    }
                    const byteArray = new Uint8Array(byteNumbers);
                    const blob = new Blob([byteArray], { type: 'application/pdf' });

                    const downloadLink = document.createElement("a");
                    downloadLink.href = URL.createObjectURL(blob);
                    downloadLink.download = data.doc.titulo;
                    downloadLink.innerText = "Ver Documento";
                    downloadLink.className = "ver-documento-btn";
                    downloadLink.style.display = "inline-block";
                    downloadLink.target = "_blank";

                    modalContent.appendChild(downloadLink);
                    modalContent.appendChild(document.createElement("br"));
                }

                const cerrarButton = document.createElement("button");
                cerrarButton.innerText = "Cerrar";
                cerrarButton.className = "paginacion-btn";
                cerrarButton.onclick = function () {
                    modal.style.display = "none";
                };
                modalContent.appendChild(cerrarButton);

                modal.style.display = "block";
                window.scrollTo({ top: 0, behavior: 'smooth' });
            })
            .catch(error => {
                console.error('Error al obtener detalles del proyecto:', error);
                alert('Hubo un problema al obtener los detalles del proyecto.');
            });
    }

    function inicializarVerProyectos() {
        obtenerProyectos();
    }

    inicializarVerProyectos();

    function mostrarProgramas() {
        const facultad = document.getElementById("facultad").value;
        const programaSelect = document.getElementById("programa");
        programaSelect.innerHTML = '<option value="null">seleccionar...</option>';

        let programas = [];

        if (facultad === "Facultad de Ciencias, Educación, Artes y Humanidades") {
            programas = [
                "Diseño Gráfico",
                "Licenciatura en Educación Básica Primaria"
            ];
        } else if (facultad === "Facultad de Ciencias Económicas y Administrativas") {
            programas = [
                "Administración de Negocios Internacionales",
                "Inteligencia de Negocios"
            ];
        } else if (facultad === "Facultad de Ingenierías") {
            programas = [
                "Ingeniería Eléctrica",
                "Ingeniería en Seguridad y Salud en el Trabajo",
                "Ingeniería Industrial",
                "Ingeniería Mecatrónica",
                "Ingeniería Telemática"
            ];
        }

        programas.forEach(programa => {
            const option = document.createElement("option");
            option.value = programa;
            option.textContent = programa;
            programaSelect.appendChild(option);
        });
    }

    function filtrar() {
        let facultad = document.getElementById('facultad').value;
        let programa = document.getElementById('programa').value;
        let estado = document.getElementById('estado-proyecto').value;
        let pagina = 1;

        if (facultad === 'null' && programa === 'null' && estado === 'null') {
            mostrarProyectos(listaProyectos, pagina); // Muestra todos los proyectos si no hay filtros
            return;
        }

        fetch(ruta + '/obtener_filtro', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                facultad: facultad,
                programa: programa,
                estado: estado,
                pagina: pagina
            })
        })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    listaProyectos = data.proyectos.sort((a, b) => b.id - a.id);
                    mostrarProyectos(listaProyectos, pagina);
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

    document.getElementById("facultad").addEventListener("change", mostrarProgramas);
    document.getElementById("filtrar").addEventListener("click", filtrar);
})();