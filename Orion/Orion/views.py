from rivescript import RiveScript
from django.http import HttpRequest


bot = RiveScript()
bot.load_file('./finanzas.rive')
bot.sort_replies()

while True:
    mensaje = input('You> ')
    #if mensaje is not None:
    if mensaje == '/quit':
        break
    reply = bot.reply('usuario', mensaje)
    print ('Bot> ', reply)

    f = open('respuesta.txt','w')
    f.write(reply)
    f.close()