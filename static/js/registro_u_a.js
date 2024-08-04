function registrar() {
    var nombre = document.getElementById('nombre').value;
    var email = document.getElementById('correo').value;
    var progra = document.getElementById('programa').value;
    var loadingModal = document.getElementById('loadingModal');


    var ruta = 'http://127.0.0.1:5000'
    if (email.includes("@unibarranquilla.edu.co")) {
        loadingModal.style.display = 'block';
        fetch(ruta + '/register_user', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ nombre: nombre, email: email, progra: progra })
        })
            .then(response => {
                if (!response.ok) {
                    return response.json().then(err => { throw new Error(err.message) });
                }
                return response.json();
            })
            .then(data => {
                if (data.success) {
                    loadingModal.style.display = 'none';
                    alert('Se ha registrado de manera exitosa.');
                } else {
                    loadingModal.style.display = 'none';
                    alert('' + data.message);
                }
            })
            .catch(error => {
                loadingModal.style.display = 'none';
                console.error('Error:', error);
                alert('Hubo un problema con el registro de su cuenta: ' + error.message);
            });

    } else {
        alert("Ingrese un correo institucional válido.");
    }
}