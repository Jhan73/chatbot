from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .crd import VERIFY_TOKEN_WHATSAPP, PAGE_ACCESS_TOKEN_WHATSAPP
from heyoo import WhatsApp
from .funciones import obtenerRespuesta, registrarChat

@csrf_exempt
def whatsAppWebhook(request):
    if request.method == 'GET':
        # La solicitud es para verificar el webhook
        mode = request.GET['hub.mode']
        token = request.GET['hub.verify_token']
        challenge = request.GET['hub.challenge']
        if mode == 'subscribe' and token == VERIFY_TOKEN_WHATSAPP:
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
    canal = "10001"
    bot_respuesta = 'OrionBot'
    if mensaje is not None:
        respuesta = obtenerRespuesta(mensaje)
        registrarChat(mensaje, respuesta, timestamp, idsms, bot_respuesta, telefonoUsuario, canal)
        enviarMensaje(telefonoUsuario, respuesta)
        return HttpResponse('success', status = 200)

def enviarMensaje (telefonoUsuario, respuesta):
    token = PAGE_ACCESS_TOKEN_WHATSAPP
    idNumeroTelefonico = '100118993079677'
    mensajeWhatsapp = WhatsApp(token, idNumeroTelefonico)
    telefonoReceptor = telefonoUsuario.replace('521','51')
    mensajeWhatsapp.send_message(respuesta, telefonoReceptor)