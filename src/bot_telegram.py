# David Valverde Gómez
# Ingeniería Informática - ULL
# alu0101100296@ull.edu.es
# Trabajo de Fin de Grado
# Generación automática de textos utilizando el modelo GPT-2 de OpenAI

# Este fichero contiene la configuración del bot de Telegram diseñado
# para mostrar los resultados de los diferentes modelos entrenados

# La idea es que, cuando se introduzca un comando determinado, el bot responda
# con un texto generado por el modelo indicado según dicho comando.

# Cuando no se introduzca ningún comando, sino se envíe un mensaje normal, ese mensaje
# se utilice como parámetro para generar texto a partir del mismo, utilizando el modelo
# entrenado por todos los ficheros de datos, de manera que se responda con un mensaje que continúe
# lo escrito por el usuario.

import os 
import sys 

# Se importan las librerías de configuración de Telegram
import logging

from telegram import Update, ForceReply
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

# Se importa la función para ejecutar los modelos
from main_functions import execute

# Activar logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)

# Se definen las funciones que manejan los comandos

# Función que retorna un mensaje de bienvenida cuando se recibe el comando /start
def start(update: Update, _: CallbackContext) -> None:
    # Se obtiene el nombre del usuario
    user = update.effective_user
    nombre_usuario = user.mention_markdown_v2()
    mensaje_saludo = fr'¡Hola, {user.mention_markdown_v2()}\!'
    update.message.reply_markdown_v2(
        mensaje_saludo
    )

    mensaje_bienvenida = '\nSoy David Valverde, y he creado este bot como complemento para mostrar mi Trabajo de Fin de Grado\n\nConsiste básicamente en la generación automática de textos, basada en varias series de libros conocidas, de forma que, con sólo introducir el comando adecuado, recibirás un texto generado automáticamente basado en el libro que elijas\n\nLos comandos son: \n-/HarryPotter\n-/LosJuegosDelHambre\n-/Narnia\n-/Crepusculo\n-/Divergente\n-/Todos\n\nAdemás, si no introduces ningún comando y envías un mensaje normal, podrás comenzar a escribir una historia propia con ayuda del bot, de manera que este continuará con lo que escribas.\n\nNOTA: El bot tarda entre 8 y 10 minutos en responder, por favor, utilizar sólo 1 comando o mensaje de cada vez'
    update.message.reply_text(mensaje_bienvenida)

# Mensaje de ayuda activado por el comando /help
def help_command(update: Update, _: CallbackContext) -> None:
    mensaje_ayuda = 'Los comandos son: \n-/HarryPotter\n-/LosJuegosDelHambre\n-/Narnia\n-/Crepusculo\n-/Divergente\n-/Todos\n\nAdemás, si no introduces ningún comando y envías un mensaje normal, podrás comenzar a escribir una historia propia con ayuda del bot, de manera que este continuará con lo que escribas.\n\nNOTA: El bot tarda entre 8 y 10 minutos en responder, por favor, utilizar sólo 1 comando o mensaje de cada vez'
    update.message.reply_text(mensaje_ayuda)

# Si se introduce un mensaje normal, se utiliza como prefijo para la ejecución del modelo
def default(update: Update, _: CallbackContext) -> None:
    mensaje = execute('Todos', words=50, prefix=update.message.text)
    #mensaje = 'No estoy preparado para reaccionar a este tipo de mensajes. Por favor, envía /help para ver la lista de comandos'
    update.message.reply_text(mensaje)
    os.execv(sys.executable, ['python3.6'] + sys.argv)


# Esta función se activa cuando se introduce algún comando relativo a los modelos implementados
# y envía como respuesta el resultado de la ejecución del modelo indicado
def generar_texto(update: Update, _: CallbackContext) -> None:
    update.message.reply_text(execute(update.message.text[1:], words=200))
    os.execv(sys.executable, ['python3.6'] + sys.argv)


def main() -> None:
    try:
        # Se accede al bot mediante su token identificativo
        updater = Updater("1877437670:AAH2Dit5e3zhM_3eqKNyL_FtpA0r3LImKYs")
        # 1778530052:AAEIvhMrfRIsEw0LFQzvdKp5zQ4SSE92UAo

        # Objeto usado para asignar las funciones que manejan los comandos
        dispatcher = updater.dispatcher

        # Se definen los comandos permitidos y se relacionan con su correspondiente función
        dispatcher.add_handler(CommandHandler("start", start))
        dispatcher.add_handler(CommandHandler("help", help_command))
        dispatcher.add_handler(CommandHandler("Divergente", generar_texto))
        dispatcher.add_handler(CommandHandler("HarryPotter", generar_texto))
        dispatcher.add_handler(CommandHandler("LosJuegosDelHambre", generar_texto))
        dispatcher.add_handler(CommandHandler("Narnia", generar_texto))
        dispatcher.add_handler(CommandHandler("Crepusculo", generar_texto))
        dispatcher.add_handler(CommandHandler("Todos", generar_texto))


        # Función asociada con los mensajes normales que no son comandos
        dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, default))

        # Se inicia el bot
        updater.start_polling()

        # El bot se ejecuta hasta que se interrumpa manualmente la ejecución con Ctrl+C
        updater.idle()

    except Exception as e:
        print(e)


if __name__ == '__main__':
    main()
