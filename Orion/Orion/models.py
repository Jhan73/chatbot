class Usuario :
    def __ini__(self):
        self.nombre = ""
        self.email = ""
        self.telefono = ""
    def get_nombre(self):
        return self._nombre
    
    def set_nombre(self, nombre):
        self._nombre = nombre

    def get_email(self):
        return self._email
    
    def set_email(self, email):
        self._email = email

    def get_telefono(self):
        return self._telefono
    
    def set_telefono(self, telefono):
        self._telefono = telefono

class Chat :
    def __init__(self, sms_recibido, sms_enviado, fecha_hora_sms_recibido, timestamp_wa, id_sms_recibido, telefono, id_chat = None) :
        self.sms_recibido = sms_recibido
        self.sms_enviado = sms_enviado
        self.fecha_hora_sms_recibido = fecha_hora_sms_recibido
        self.timestamp_wa = timestamp_wa
        self.id_sms_recibido = id_sms_recibido
        self.telefono_usuario = telefono
