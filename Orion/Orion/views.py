from django.http import HttpRequest, HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from rivescript import RiveScript
import psycopg2
from heyoo import WhatsApp

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
    #elif request.method == 'POST':
    data = json.loads(request.body)
    idusuario = data['entry'][0]['id']
    telefonoUsuario = data['entry'][0]['changes'][0]['value']['messages'][0]['from']
    #Extraemos el cuerpo del mensaje
    mensaje = data['entry'][0]['changes'][0]['value']['messages'][0]['text']['body']
    #extraemos el ID de whatsapp del array
    idsms = data['entry'][0]['changes'][0]['value']['messages'][0]['id']
    #estraemos el tiempo de whatsapp del array
    timestamp = data['entry'][0]['changes'][0]['value']['messages'][0]['timestamp']
    #return HttpResponse('success', status = 200)
    estructure = open("estructura.txt",'w')
    estructure.write(json.dumps(data))
    estructure.close()
    if mensaje is not None:
        bot = RiveScript()
        bot.load_file('./finanzas.rive')
        bot.sort_replies()

        respuesta = bot.reply("localuser", mensaje)
        respuesta = respuesta.replace('\\n','\\\n')
        respuesta = respuesta.replace('\\','')
        #CONECCION A BASE DE DATOS

        try :
            connection = psycopg2.connect(
                host = 'postgresql-jhan.alwaysdata.net',
                user = 'jhan',
                password = 'Labradoodle24',
                database = 'jhan_orion'
            )

            cursor = connection.cursor()

            cursor.execute('SELECT version()')
            row1 = cursor.fetchone()
            file1 = open("texto1.txt",'w')
            file1.write(str(row1))
            file1.close()

            query = ("SELECT count(id_chat) AS cantidad FROM chats WHERE id_sms_recibido = '"+idsms +"'")
            cursor.execute(query)
            cantidad, = cursor.fetchone()
            cantidad = int(str(cantidad))

            if cantidad == 0:
                sql = ("INSERT INTO chats " + 
                       "(sms_recibido, sms_enviado, timestamp_wa, id_sms_recibido, id_usuario) VALUES "+
                       "(%s, %s, %s, %s, %s)")
                cursor.execute(sql, (mensaje, respuesta, int(timestamp), idsms, idusuario))
                connection.commit()
                enviarMensaje(telefonoUsuario, respuesta)
        except Exception as ex:
            return HttpResponse('error sql')
        finally:
            connection.close()

        #ARCHIVO DE ALMACENAMIENTO
        file = open("texto.txt",'w')
        file.write(mensaje)
        file.close()
        estructura = open("respuesta.txt",'w')
        estructura.write(respuesta)
        estructura.close()
        return HttpResponse('success', status = 200)
    
def enviarMensaje (telefonoUsuario, respuesta):
    token = 'EAAUORvahOyEBAH0Ta6rsJYly10kMNe4ZC5G23sFvBQWz7TaDZA2A7DdZBFq99xdEeWx7Uc8ZBVrmLYD5fjv2Vxzhizhl1TwbZBqQ8PVetorlOJDhMErUcbZCpZAMTJu3KZANHFAG9wkR0UStqIcPeQsZAQsTMp9yacUCSe0oKZCZAqDZCWgd7XMTobNNpQ1KrKKZBIulE4G2Pa6TeLgZDZD'
    idNumeroTelefonico = '100118993079677'
    mensajeWhatsapp = WhatsApp(token, idNumeroTelefonico)
    telefonoReceptor = telefonoUsuario.replace('521','51')
    mensajeWhatsapp.send_message(respuesta, telefonoReceptor)