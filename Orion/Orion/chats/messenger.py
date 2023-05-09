from django.shortcuts import render
from django.http import  HttpResponse
import json
from django.views.decorators.csrf import csrf_exempt
from .funciones import obtenerRespuesta, registrarChat
from datetime import datetime
from .crd import VERIFY_TOKEN_MESSENGER, PAGE_ACCESS_TOKEN_MESSENGER
import requests

def messengerConnection(request):
    return render(request, 'messenger.html')

@csrf_exempt
def messengerWebhook(request):
    if request.method == 'GET':
        # La solicitud es para verificar el webhook
        mode = request.GET.get('hub.mode')
        token = request.GET.get('hub.verify_token')
        challenge = request.GET.get('hub.challenge')
        if mode == 'subscribe' and token == VERIFY_TOKEN_MESSENGER:
            # Respondemos con el token de verificación enviado por Facebook
            return HttpResponse(challenge, status = 200)
        else:
            # Si el token de verificación no coincide, respondemos con un error 403
            return HttpResponse('no se pudo conectar', status = 403)
    elif request.method == 'POST':
        body = request.body.decode('utf-8')
        # Cargar el JSON enviado por Facebook
        data = json.loads(request.body)
        # Guardar solo los campos necesarios en una base de datos o archivo
        mensaje = data.get('entry')[0].get('messaging')[0].get('message').get('text')
        idsms = data.get('entry')[0].get('messaging')[0].get('sender').get('id')
        idmessenger = data.get('entry')[0].get('messaging')[0].get('recipient').get('id')


        respuesta = obtenerRespuesta(mensaje)
        fecha_actual = datetime.now()
        fecha_unix = int(fecha_actual.timestamp())
        timestamp = str(fecha_unix)
        telefonoUsuario = '51989898989'
        canal = '10004'
        registrarChat(mensaje, respuesta, timestamp, idsms, telefonoUsuario, canal)
        sendMessage(idmessenger, respuesta)
        
        return HttpResponse('ok', status=200)

def sendMessage(idmessenger, respuesta):
    data = {
        "recipient": {"id": idmessenger},
        "message": {"text": respuesta}
    }
    params = {
        "access_token": PAGE_ACCESS_TOKEN_MESSENGER
    }
    headers = {
        "Content-Type": "application/json"
    }
    r = requests.post("https://graph.facebook.com/v10.0/me/messages", params=params, headers=headers, json=data)
    if r.status_code != 200:
        print(r.status_code)
        print(r.text)