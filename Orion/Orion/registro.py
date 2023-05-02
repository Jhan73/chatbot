from django.shortcuts import render
from django.http import HttpResponse
import psycopg2
import random
from .crd import password, pasm
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
            enviarCorreo(usuario.get_email(), tokenGenerado)
            return render(request, 'auth.html',{'email': usuario.get_email()})
    return render(request, 'login.html')
inputToken = 0
def autenticacion (request):

    if request.method == 'POST':
        if request.POST['token']:
            global inputToken
            global tokenValidado
            inputToken = int(request.POST['token'])
            if inputToken == tokenGenerado:
                registrarUsuario(usuario.get_nombre(),usuario.get_email(), usuario.get_telefono())
                return render(request,'confirmacion.html',{'nombre':usuario.get_nombre()})
            else:
                tokenValidado = not tokenValidado
                return render(request, 'auth.html', {'email': usuario.get_email(), 'tokenInvalido': tokenValidado})
    return render(request, 'auth.html', {'nombre': usuario.get_nombre(), 'tokenInvalido': tokenValidado})

def confirmacion(request):
    return render(request, 'confirmacion.html')

def enviarCorreo (email_usuario, token):
    import yagmail
    email = 'antezana241197@gmail.com'
    contra = pasm
    yag = yagmail.SMTP(user=email, password=contra)
    destinatarios = [email_usuario]

    asunto = 'Código de verificación'
    mensaje = 'El código de verificación es: {}'.format( token)
    yag.send(destinatarios, asunto, mensaje)

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