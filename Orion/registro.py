from django.shortcuts import render
from django.http import HttpResponse
import psycopg2
import random
from .crd import password, pasm
import smtplib
import email.mime.multipart#.......
import email.mime.base#.......
from email.mime.text import MIMEText#..............
from email.message import EmailMessage
import ssl
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
            enviarCorreo(usuario.get_email, usuario.get_nombre, tokenGenerado)
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

def enviarCorreo (email_usuario,nombre_usuario, token):
    email_emisor = 'antezana241197@gmail.com'
    email_contrasenia = pasm
    email_receptor = email_usuario
    asunto = 'Código de confirmación'
    cuerpo = "Hola {}, el código de confirmación es: {}".format(nombre_usuario, token)
    em = EmailMessage()
    em['From'] = email_emisor
    em['To'] = email_receptor
    em['Subject'] = asunto
    em.set_content(cuerpo)
    contexto = ssl.create_default_context()
    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=contexto) as smtp:
        smtp.login(email_emisor, email_contrasenia)
        smtp.sendmail(email_emisor, email_receptor, em.as_string())

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