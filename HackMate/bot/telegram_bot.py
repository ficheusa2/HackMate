# bot/telegram_bot.py
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, CallbackContext
from db.db_connector import fetch_users
from matcher.matcher import matching_algorithm

# Configuración de logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

TOKEN = "TU_TOKEN_DEL_BOT"  # Reemplaza por tu token real

async def match_command(update: Update, context: CallbackContext):
    # Comando que puede ser usado por el admin para ejecutar el matching
    users = fetch_users()  # Obtén la lista de usuarios desde la DB
    matches = matching_algorithm(users)
    response = "Resultados de Matching:\n"
    for match in matches:
        response += f"Usuario {match[0]} emparejado con Usuario {match[1]} (Score: {match[2]:.2f})\n"
    await update.message.reply_text(response)
    # Aquí también puedes añadir la lógica para guardar los matches en la DB

def main():
    application = Application.builder().token(TOKEN).build()
    application.add_handler(CommandHandler("match", match_command))
    application.run_polling()

if __name__ == "__main__":
    main()
