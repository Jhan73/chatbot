from django.http import HttpRequest, HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .crd import password
from rivescript import RiveScript
import psycopg2
from heyoo import WhatsApp
import string
from unidecode import unidecode

@csrf_exempt
def whatsAppWebhook(request):
    if request.method == 'GET':
        # La solicitud es para verificar el webhook
        mode = request.GET['hub.mode']
        token = request.GET['hub.verify_token']
        challenge = request.GET['hub.challenge']
        if mode == 'subscribe' and token == 'meatyhamhock':
            # Respondemos con el token de verificación enviado por Facebook
            return HttpResponse(challenge, status = 200)
        else:
            # Si el token de verificación no coincide, respondemos con un error 403
            return HttpResponse('no se pudo conectar', status = 403)
    data = json.loads(request.body)

    #Obtención de datos del mensaje de Whatsapp
    telefonoUsuario = data['entry'][0]['changes'][0]['value']['messages'][0]['from']
    mensaje = data['entry'][0]['changes'][0]['value']['messages'][0]['text']['body']
    idsms = data['entry'][0]['changes'][0]['value']['messages'][0]['id']#extraemos el ID de whatsapp del array
    timestamp = data['entry'][0]['changes'][0]['value']['messages'][0]['timestamp']

    if mensaje is not None:
        respuesta = obtenerRespuesta(mensaje)
        registrarChat(mensaje, respuesta, timestamp, idsms, telefonoUsuario)
        return HttpResponse('success', status = 200)
def obtenerRespuesta(mensaje):

    bot = RiveScript()
    bot.load_file('./QA.rive')
    bot.sort_replies()

    puntuacion = string.punctuation
    lowerSinPuntuacion = unidecode((''.join(caracter for caracter in mensaje if caracter not in puntuacion)).lower())

    respuesta = bot.reply("localuser", lowerSinPuntuacion)
    respuesta = respuesta.replace('\\n','\\\n')
    respuesta = respuesta.replace('\\','')

    return respuesta    

def registrarChat(mensaje, respuesta, timestamp, idsms, telefonoUsuario):
    try :
        connection = psycopg2.connect(
            host = 'postgresql-jhan.alwaysdata.net',
            user = 'jhan',
            password = password,
            database = 'jhan_orion'
        )

        cursor = connection.cursor()

        query = ("SELECT count(id_chat) AS cantidad FROM chats WHERE id_sms_recibido = '" + idsms +"'")
        cursor.execute(query)
        cantidad, = cursor.fetchone()
        cantidad = int(str(cantidad))
        
        if cantidad == 0:
            sql = ("INSERT INTO chats " + 
                   "(sms_recibido, sms_enviado, timestamp_wa, id_sms_recibido, telefono_usuario) VALUES "+
                   "(%s, %s, %s, %s, %s)")
            cursor.execute(sql, (mensaje, respuesta, int(timestamp), idsms, telefonoUsuario))
            connection.commit()
            enviarMensaje(telefonoUsuario, respuesta)
    except Exception as ex:
        pass
    finally:
        connection.close()

def enviarMensaje (telefonoUsuario, respuesta):
    token = 'EAAUORvahOyEBAH0Ta6rsJYly10kMNe4ZC5G23sFvBQWz7TaDZA2A7DdZBFq99xdEeWx7Uc8ZBVrmLYD5fjv2Vxzhizhl1TwbZBqQ8PVetorlOJDhMErUcbZCpZAMTJu3KZANHFAG9wkR0UStqIcPeQsZAQsTMp9yacUCSe0oKZCZAqDZCWgd7XMTobNNpQ1KrKKZBIulE4G2Pa6TeLgZDZD'
    idNumeroTelefonico = '100118993079677'
    mensajeWhatsapp = WhatsApp(token, idNumeroTelefonico)
    telefonoReceptor = telefonoUsuario.replace('521','51')
    mensajeWhatsapp.send_message(respuesta, telefonoReceptor)