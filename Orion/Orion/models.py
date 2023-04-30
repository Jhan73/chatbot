class Usuario :
    def __init__(self, nombre, email, telefono):
        self.nombre = nombre
        self.email = email
        self.telefono = telefono

class Chat :
    def __init__(self, sms_recibido, sms_enviado, fecha_hora_sms_recibido, timestamp_wa, id_sms_recibido, telefono, id_chat = None) :
        self.sms_recibido = sms_recibido
        self.sms_enviado = sms_enviado
        self.fecha_hora_sms_recibido = fecha_hora_sms_recibido
        self.timestamp_wa = timestamp_wa
        self.id_sms_recibido = id_sms_recibido
        self.telefono_usuario = telefono
