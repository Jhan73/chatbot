from django.shortcuts import render
from django.http import HttpResponse
import psycopg2
import random
from .crd import password, pasm
import smtplib
import email.mime.multipart
import email.mime.base
from email.mime.text import MIMEText
from .models import Usuario

def home(request):
    return render(request, 'home.html')
tokenGenerado = 0
usuario = Usuario()
tokenValidado = False
def login(request):
    if request.method == 'POST':
        if request.POST['nombre'] and request.POST['email'] and request.POST['telefono']:
            global usuario
            usuario.set_nombre(request.POST['nombre'])
            usuario.set_email(request.POST['email'])
            usuario.set_telefono(request.POST['telefono'])
            global tokenGenerado
            tokenGenerado = random.randint(1000,9999)
            return render(request, 'auth.html',{'email': usuario.get_email()})
    return render(request, 'login.html')
inputToken = 0
def autenticacion (request):

    if request.method == 'POST':
        if request.POST['token']:
            global inputToken
            global tokenValidado
            inputToken = int(request.POST['token'])
            print('input token', type(inputToken) )
            if inputToken == tokenGenerado:
                registrarUsuario(usuario.get_nombre(), usuario.get_email(), usuario.get_telefono())
                return render(request,'confirmacion.html',{'nombre':usuario.get_nombre()})
            else:
                tokenValidado = not tokenValidado
                return render(request, 'auth.html', {'email': usuario.get_email(), 'tokenInvalido': tokenValidado})
    return render(request, 'auth.html', {'nombre': usuario.get_nombre(), 'tokenInvalido': tokenValidado})

def confirmacion(request):
    return render(request, 'confirmacion.html')

def enviarCorreo (email_receptor,nombre_usuario, token):
    # Crea la conexión SMTP
    server = smtplib.SMTP('smtp.gmail.com', 587)

    correo = 'antezana241197@gmail.com'
    pas = pasm
    # Inicia sesión en tu cuenta de Gmail
    server.starttls()

    server.login(correo, pas)

    # Definir el remitente y destinatario del correo electrónico
    remitente = "antezana241197@gmail.com"
    destinatario = email_receptor

    mensaje = email.mime.multipart.MIMEMultipart()
    mensaje['From'] = remitente
    mensaje['To'] = destinatario
    mensaje['Subject'] = "Codigo de verificacion"

    # Añadir el cuerpo del mensaje
    cuerpo = "Hola, %s tu código de confirmación es : %s",(nombre_usuario,token)
    mensaje.attach(email.mime.text.MIMEText(cuerpo, 'plain'))

    # Convertir el mensaje a texto plano
    texto = mensaje.as_string()

    # Enviar el correo electrónico
    server.sendmail(remitente, destinatario, texto)

    # Cerrar la conexión SMTP
    server.quit()

def registrarUsuario(nombre, email, telefono):
    try :
        connection = psycopg2.connect(
            host = 'postgresql-jhan.alwaysdata.net',
            user = 'jhan',
            password = password,
            database = 'jhan_orion'
        )
        cursor = connection.cursor()

        sql = ("INSERT INTO usuarios (telefono, nombre, email) VALUES (%s, %s, %s)")
        cursor.execute(sql, (('51'+telefono), nombre, email))
        connection.commit()
    except Exception as ex:
        pass
    finally:
        connection.close()