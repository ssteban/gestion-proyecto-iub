document.addEventListener('DOMContentLoaded', function() {
    document.getElementById('send-email').addEventListener('submit', function(event) {
        event.preventDefault()

        var correo=document.getElementById('email').value;
        var ruta='http://127.0.0.1:5000'


        fetch(ruta+'/send-mail', {  
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ correo: correo })
        })
        .then(response => {
            if (!response.ok) {
                return response.json().then(err => { throw new Error(err.message) });
            }
            return response.json();
        })
        .then(data => {
            if (data.success) {
                alert("correo enviado exitosamente. ");
                window.location.href = '../../index.html';
            } else {
                alert('Lo sentimos, no pudimos enviar el correo electronico. verifique su correo');
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('Hubo un problema con el envio del correo: ' + error.message);
        });
    });
});