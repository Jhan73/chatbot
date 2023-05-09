from django.http import JsonResponse
from .funciones import registrarChat, obtenerRespuesta
from datetime import datetime
import random
import string

def chatweb(request):
    if request.method == 'GET':
        inputMessage = request.GET["mensaje"]
        respuesta = obtenerRespuesta(inputMessage)
        data = {'mensaje': respuesta}
        fecha_actual = datetime.now()
        fecha_unix = int(fecha_actual.timestamp())
        timestamp = str(fecha_unix)
        caracteres = string.ascii_letters
        idsms = ''.join(random.choice(caracteres) for _ in range(50))
        bot_respuesta = 'OrionBot'
        telefonoUsuario = '51999999999'
        canal = '10003'
        registrarChat(inputMessage, respuesta, timestamp, idsms, bot_respuesta, telefonoUsuario, canal)
        return JsonResponse(data)
