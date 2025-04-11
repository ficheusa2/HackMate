import logging
import re
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ConversationHandler, CallbackContext
from datetime import datetime

# Configurar logging
logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)

# Token del bot (reemplaza con el real)
TOKEN = "xxxxx" 
BOT_NAME = "OnBoardHack"

# Estados de la conversación
NAME, LINKEDIN = range(2)

def save_user_response(user_id, text):
    """Guarda la respuesta del usuario en un archivo de texto."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    filename = f"{user_id}.txt"
    with open(filename, "a", encoding="utf-8") as file:
        file.write(f"[{timestamp}] {text}\n")
        file.write(f"[{timestamp}] bot_name: {BOT_NAME.lower()}\n")


async def start(update: Update, context: CallbackContext) -> int:
    """Inicia el proceso de onboarding."""
    user = update.message.from_user
    context.user_data['telegram_id'] = user.id  # Guarda el ID de Telegram
    
    message = (
        "Hola " + user.username +"!\n\nSoy un bot el 'el HackMate' te conecto con quien necesitas para crear un equipo la Hackaton.\n\n"
        "¿Me podés decir tu nombre?"
    )
    await update.message.reply_text(message)
    save_user_response(user.id, f"UserName: {user.username} ")

    return NAME

async def get_name(update: Update, context: CallbackContext) -> int:
    """Obtiene el nombre del participante."""
    user_id = update.message.from_user.id
    context.user_data['name'] = update.message.text

    save_user_response(user_id, f"Nombre: {update.message.text}")

    message = (
        "¡Genial!\n\n"
        "Contame cuál es tu perfil\nY que es lo que estás buscando o necesitando\n\n"
        "Si me compartes esta info puedo contactarte el perfil que necesites para la Hackaton.\n\n"
        
    )
    await update.message.reply_text(message)

    return LINKEDIN

async def get_linkedin(update: Update, context: CallbackContext) -> int:
    """Valida y guarda la URL de LinkedIn."""
    user_id = update.message.from_user.id
    linkedin_url = update.message.text
    save_user_response(user_id, f"Profile: {linkedin_url}")

    context.user_data['linkedin'] = linkedin_url

    message = (
        "¡Excelente! Ni bien tengamos tu Match te contactamos por aqui.\n\n"
        "Ha finalizado la conversación. P\n\nNos vemos! "
    )
    await update.message.reply_text(message)

    return ConversationHandler.END  # Finaliza la conversación

async def cancel(update: Update, context: CallbackContext) -> int:
    """Permite cancelar la conversación."""
    await update.message.reply_text("Has cancelado la conversación. ¡Nos vemos pronto!")
    return ConversationHandler.END  # Finaliza la conversación

def main():
    """Función principal que ejecuta el bot."""
    application = Application.builder().token(TOKEN).build()

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_name)],
            LINKEDIN: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_linkedin)],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )

    application.add_handler(conv_handler)
    application.run_polling()

if __name__ == "__main__":
    main()


