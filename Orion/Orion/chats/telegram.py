from django.shortcuts import render
import telebot
from .funciones import registrarChat, obtenerRespuesta
from .crd import TELEGRAM_BOT_ID, SERVER_PASSWORD
import psycopg2

bot  = telebot.TeleBot(TELEGRAM_BOT_ID)
span = '@gmail.com'
def telegramConnetion(request):
    return render(request, 'Telegram.html')

@bot.message_handler(commands=['help', 'start'])
def enviar (message):
    bot.reply_to(message, 'Hola, como estas?')

@bot.message_handler(func=lambda message: True)
def mensaje(message):
    canal = '10002'
    bot_respuesta = 'OrionBot'
    mensaje = message.json["text"]
    idsms = str(message.message_id)
    timestamp = str(message.date)
    nombre = message.from_user['username']
    telefonoUsuario = str(message.chat.id)
    respuesta = obtenerRespuesta(mensaje)
    if existeUsuario(telefonoUsuario) == 0:
        registrarUsuario(telefonoUsuario, nombre)
    registrarChat(mensaje, respuesta, timestamp, idsms, bot_respuesta, telefonoUsuario, canal)
    bot.reply_to(message, respuesta)
def existeUsuario(telefonoUsuario):
    connection = psycopg2.connect(
        host = 'postgresql-jhan.alwaysdata.net',
        user = 'jhan',
        password = SERVER_PASSWORD,
        database = 'jhan_orion'
    )

    cursor = connection.cursor()

    query = ("SELECT count(id_chat) AS cantidad FROM usuarios WHERE telefono = '" + telefonoUsuario +"'")
    cursor.execute(query)
    cantidad, = cursor.fetchone()
    cantidad = int(str(cantidad))
    return cantidad
def registrarUsuario(telefonoUsuario, nombre):
    connection = psycopg2.connect(
        host = 'postgresql-jhan.alwaysdata.net',
        user = 'jhan',
        password = SERVER_PASSWORD,
        database = 'jhan_orion'
    )
    cursor = connection.cursor()
    email = nombre + span
    sql = ("INSERT INTO usuarios (telefono, nombre, email) VALUES (%s, %s, %s)")
    cursor.execute(sql, (telefonoUsuario, nombre, email))
    connection.commit()
bot.polling()




