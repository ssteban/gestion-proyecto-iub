document.addEventListener("DOMContentLoaded", function() {
    const contenidoDiv = document.getElementById("contenido");

    var ruta='http://127.0.0.1:5000'

    function loadContent(url, callback) {
        fetch(url)
            .then(response => {
                if (!response.ok) {
                    throw new Error(`HTTP error! status: ${response.status}`);
                }
                return response.text();
            })
            .then(data => {
                contenidoDiv.innerHTML = data;
                if (callback) callback();
            })
            .catch(error => {
                contenidoDiv.innerHTML = `<p>Error al cargar el contenido: ${error.message}</p>`;
            });
    }

    function loadScript(url, callback) {
        const script = document.createElement('script');
        script.src = url;
        script.onload = callback;
        document.head.appendChild(script);
    }

    obtener_informacion();

    document.getElementById("ver-proyectos").addEventListener("click", function(event) {
        event.preventDefault();
        loadContent('ver-proyectos.html', function() {
            loadScript('/static/js/ver-proyecto.js', function() {
                console.log('Script de ver-proyecto.js cargado y ejecutado.');
            });
        });
    });

    document.getElementById("ver-proyectos2").addEventListener("click", function(event) {
        event.preventDefault();
        loadContent('ver-proyectos.html', function() {
            loadScript('/static/js/ver-proyecto.js', function() {
                console.log('Script de ver-proyecto.js cargado y ejecutado.');
            });
        });
    });

    document.getElementById("registrar-proyectos").addEventListener("click", function(event) {
        event.preventDefault();
        loadContent('registro-p.html', function() {
            loadScript('/static/js/registro-p.js', function() {
                console.log('Script de registro-p.js cargado y ejecutado.');
            });
        });
    });

    document.getElementById("mis-proyectos").addEventListener("click", function(event) {
        event.preventDefault();
        loadContent('mis-proyectos.html', function() {
            loadScript('/static/js/mis-proyectos.js', function() {
                console.log('Script de mis-proyectos.js cargado y ejecutado.');
            });
        });
    });


    document.getElementById("tendencias").addEventListener("click", function(event) {
        event.preventDefault();
        loadContent('tendencias.html', function() {
            loadScript('https://code.highcharts.com/highcharts.js', function() {
                console.log('Script de tendencias.js cargado y ejecutado 1.');
                loadScript('https://code.highcharts.com/modules/drilldown.js', function() {
                    console.log('Script de tendencias.js cargado y ejecutado 2.');
                    loadScript('/static/js/tendencias.js', function() {
                        console.log('Script de tendencias.js cargado y ejecutado.');
                    });
                });
            });
        });
    });

    document.getElementById("perfil").addEventListener("click", function(event) {
        event.preventDefault();
        loadContent('perfil-u.html', function(){
            loadScript('/static/js/perfil-u.js', function(){
                console.log('scrip de perfil cargado con exito')
            })
        });
    });

    document.getElementById("cerrar-sesion").addEventListener("click", function(event) {
        event.preventDefault();
                if (confirm("¿Seguro que desea cerrar sesión?")) {
                    const loggedInUser = JSON.parse(localStorage.getItem('loggedInUser'));
                    if (loggedInUser) {
                        localStorage.removeItem('loggedInUser');
                        window.location.href = '../../index.html'; 
                    }
            }
    });

    // Cargar contenido inicial
    loadContent('ver-proyectos.html', function() {
        loadScript('/static/js/ver-proyecto.js', function() {
            console.log('Script de ver-proyecto.js cargado y ejecutado.');
        });
    });



//cargar foto de perfil
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
            // Actualizar la imagen de perfil
            if (data.datos.foto) {
                document.getElementById('img_user').src = 'data:image/png;base64,' + data.datos.foto;
            }
        })
        .catch(error => {
            loadingModal.style.display = 'none';
            console.error('Error al obtener los datos del estudiante:', error);
        });
    }


});



//verificar que la sesion exista
function checkLogin(){
    const loggedInUser = JSON.parse(localStorage.getItem('loggedInUser'));
    if (!loggedInUser) {
        setTimeout(function() {
            window.location.href = '../../index.html';
//            return false;
        }, 1000);
    }else{
        return true
    }
}


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
        // Actualizar la imagen de perfil
        if (data.datos.foto) {
            document.getElementById('img_user').src = 'data:image/png;base64,' + data.datos.foto;
        }
    })
    .catch(error => {
        loadingModal.style.display = 'none';
        console.error('Error al obtener los datos del estudiante:', error);
    });
}

