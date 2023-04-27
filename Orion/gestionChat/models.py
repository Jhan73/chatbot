from django.db import models

class Usuario(models.Model):
    nombre = models.CharField(max_length=30)
    email = models.EmailField()
    telefono = models.CharField(max_length=15)

class Chat (models.Model):

    mensaje_recibido = models.CharField(max_length=255)
    mendaje_enviado = models.CharField(max_length=255)
    id_usuario = models.IntegerField()
    fecha_hora_sms_recibido = models.DateTimeField()
    timestamp_wa = models.IntegerField()
    