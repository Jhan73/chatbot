from .crd import SERVER_PASSWORD, CHATGPT_API_KEY
from rivescript import RiveScript
import psycopg2
import string
from unidecode import unidecode
import openai

bot_respuesta = 'OrionBot'
def obtenerRespuesta(mensaje):

    bot = RiveScript()
    bot.load_file('./QA.rive')
    bot.sort_replies()

    puntuacion = string.punctuation
    lowerSinPuntuacion = unidecode((''.join(caracter for caracter in mensaje if caracter not in puntuacion)).lower())

    respuesta = bot.reply("localuser", lowerSinPuntuacion)
    respuesta = respuesta.replace('\\n','\\\n')
    respuesta = respuesta.replace('\\','')
    if respuesta == "error":
        respuesta = obtenerRespuestaConChatGPT(mensaje)
        global bot_respuesta
        bot_respuesta = 'ChatGPT'
    return respuesta    

def registrarChat(mensaje, respuesta, timestamp, idsms, telefonoUsuario, canal):
    try :
        connection = psycopg2.connect(
            host = 'postgresql-jhan.alwaysdata.net',
            user = 'jhan',
            password = SERVER_PASSWORD,
            database = 'jhan_orion'
        )

        cursor = connection.cursor()

        query = ("SELECT count(id_chat) AS cantidad FROM chats WHERE id_sms_recibido = '" + idsms +"'")
        cursor.execute(query)
        cantidad, = cursor.fetchone()
        cantidad = int(str(cantidad))
        
        if cantidad == 0:
            sql = ("INSERT INTO chats " + 
                   "(sms_recibido, sms_enviado, timestamp_procesado, id_sms_recibido, bot_respuesta, telefono_usuario, id_canal) VALUES "+
                   "(%s, %s, %s, %s, %s, %s, %s)")
            cursor.execute(sql, (mensaje, respuesta, int(timestamp), idsms, bot_respuesta, telefonoUsuario, canal))
            connection.commit()
    except Exception as ex:
        print(ex)
    finally:
        connection.close()

def obtenerRespuestaConChatGPT(prompt):
    openai.api_key = CHATGPT_API_KEY
    completion = openai.Completion.create(
        engine = "text-davinci-003",
        prompt = prompt,
        max_tokens = 1024,
        n = 1,
        stop = None,
        temperature = 0.7,
    )
    response = completion.choices[0].text
    return response