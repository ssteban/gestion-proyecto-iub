from email.message import EmailMessage
import smtplib

# Credenciales
remitente = "gestionproyectoiub@gmail.com"
password = "zhrdwyggrbhqprmh" 


destinatario = "fidelsangon@gmail.com"
mensaje = f"""
    mensaje de recuperacion de contraseña
"""


email = EmailMessage()
email["From"] = remitente
email["To"] = destinatario
email["Subject"] = "Recuperacion de Contraseña"
email.set_content(mensaje)


try:
    smtp = smtplib.SMTP("smtp.office365.com", port=587)
    smtp.starttls()
    smtp.login(remitente, password)
    smtp.sendmail(remitente, destinatario, email.as_string())
    smtp.quit()
    print("Correo enviado exitosamente")
except Exception as e:
    print(f"Error al enviar correo: {e}")
