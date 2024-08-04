console.log("El archivo JS de registro-p.js se cargó correctamente");

var palabrasClaves = [];

function registrarProyecto() {
    console.log("Obteniendo datos...");

    var titulo = document.getElementById("titulo").value.trim();
    var resumen = document.getElementById("resumen").value.trim();
    var facultad = document.getElementById("facultad").value;
    var programa = document.getElementById("programa").value;
    var tipoProyecto = document.getElementById("tipo-proyecto").value;
    var estadoProyecto = document.getElementById("estado-proyecto").value;
    var estudiantes = document.getElementById("estudiantes").value.trim();
    var docente = document.getElementById("docente").value.trim();

    // Validación de campos vacíos
    if (!titulo || !resumen || facultad === "null" || tipoProyecto === "null" || palabrasClaves.length === 0 || estadoProyecto === "null" || !estudiantes || !docente) {
        alert("Por favor, complete todos los campos antes de registrar el proyecto.");
        return;
    }

    var ruta = 'http://127.0.0.1:5000';
    const correoUsuario = JSON.parse(localStorage.getItem('loggedInUser'));
    fetch(ruta + '/register-p', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            titulo: titulo,
            resumen: resumen,
            facultad: facultad,
            programa: programa,
            tipoProyecto: tipoProyecto,
            palabrasClaves: palabrasClaves.join(','),
            estadoProyecto: estadoProyecto,
            estudiantes: estudiantes,
            docente: docente,
            registrado: correoUsuario.user
        })
    })
    .then(response => {
        if (!response.ok) {
            return response.json().then(err => { throw new Error(err.message) });
        }
        return response.json();
    })
    .then(data => {
        if (data.success) {
            alert('Se ha registrado el proyecto de manera exitosa.');
            // Limpiar campos
            document.getElementById("titulo").value = "";
            document.getElementById("resumen").value = "";
            document.getElementById("facultad").selectedIndex = 0;
            document.getElementById("programa").selectedIndex = 0;
            document.getElementById("tipo-proyecto").selectedIndex = 0;
            document.getElementById("palabras-claves").value = "";
            document.getElementById("estado-proyecto").selectedIndex = 0;
            document.getElementById("estudiantes").value = "";
            document.getElementById("docente").value = "";
            palabrasClaves = [];
            actualizarListaPalabrasClaves();
        } else {
            alert('Hubo un error al registrar el proyecto: ' + data.message);
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('Hubo un problema con el registro del proyecto: ' + error.message);
    });
}

function addPalabraClave() {
    const palabraClaveInput = document.getElementById('palabras-claves');
    const palabraClave = palabraClaveInput.value.trim();

    if (palabraClave) {
        palabrasClaves.push(palabraClave);
        actualizarListaPalabrasClaves();
        palabraClaveInput.value = ''; // Limpiar el campo de entrada
    }
}

function actualizarListaPalabrasClaves() {
    const lista = document.getElementById('lista-palabras-claves');
    lista.innerHTML = '';
    palabrasClaves.forEach((palabra, index) => {
        const palabraElemento = document.createElement('div');
        palabraElemento.textContent = palabra;
        palabraElemento.classList.add('palabra-clave');
        lista.appendChild(palabraElemento);
    });
}


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
        console.log(programas)
    } else if (facultad === "Facultad de Ciencias Económicas y Administrativas") {
        programas = [
            "Administración de Negocios Internacionales",
            "Inteligencia de Negocios"
        ];
        console.log(programas)
    } else if (facultad === "Facultad de Ingenierías") {
        programas = [
            "Ingeniería Eléctrica",
            "Ingeniería en Seguridad y Salud en el Trabajo",
            "Ingeniería Industrial",
            "Ingeniería Mecatrónica",
            "Ingeniería Telemática"
        ];
        console.log(programas)
    }

    programas.forEach(programa => {
        const option = document.createElement("option");
        option.value = programa;
        option.textContent = programa;
        programaSelect.appendChild(option);
    });
}
