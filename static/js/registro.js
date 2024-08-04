document.addEventListener('DOMContentLoaded', function() {
    document.getElementById('register-form').addEventListener('submit', function(event) {
        event.preventDefault();

        var nombre = document.getElementById('nombre').value;
        var email = document.getElementById('correo').value;
        var progra = document.getElementById('programa').value;
        var pass1 = document.getElementById('contra1').value;
        var pass2 = document.getElementById('contra2').value;
        var loadingModal = document.getElementById('loadingModal');
    

        var ruta='http://127.0.0.1:5000'
        if (pass1.length > 5 && pass1.length < 13) {
            console.log(pass1.length)
            if (pass1 === pass2) {
                if (email.includes("@unibarranquilla.edu.co")) {
                    loadingModal.style.display = 'block';
                    fetch(ruta+'/register', {  
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json'
                        },
                        body: JSON.stringify({ nombre: nombre, email: email, progra: progra, pass1: pass1 })
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
                            window.location.href = '../../index.html';
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
            } else {
                alert("Las contraseñas no son iguales. Confírmelas.");
            }
        }else{
            alert("La contraseña debe tener entre 6 y 12 caracteres.");
        }
    });
});
