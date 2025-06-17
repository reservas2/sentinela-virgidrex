import os
import logging
import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
from dotenv import load_dotenv

load_dotenv()
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
BSCSCAN_API = os.getenv("BSCSCAN_API_KEY")
TOKEN_ADDRESS = os.getenv("TOKEN_ADDRESS")
def get_env_var(var_name, default_value=None, is_int=False):
    value = os.getenv(var_name, default_value)
    
    # Se for uma string com ${...}, é inválido
    if value and value.startswith("${") and value.endswith("}"):
        print(f"⚠️ Variável {var_name} não foi configurada corretamente. Usando valor padrão.")
        value = default_value
    
    if is_int and value:
        try:
            return int(value)
        except ValueError:
            print(f"❌ Erro ao converter {var_name} para inteiro: {value}")
            return int(default_value or 0)
    
    return value

MAX_TOKENS = get_env_var("MAX_TOKENS", "300000000000000000000000", is_int=True)
GRUPO_HOLDERS = os.getenv("GRUPO_HOLDERS")
GRUPO_ESPERA = os.getenv("GRUPO_ESPERA")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👋 Envie sua carteira BSC (ex: 0x...) ou um print do saldo para ser validado.")

# ... (funções de validação e handlers de carteira/foto/help)

if __name__ == "__main__":
    if not BOT_TOKEN:
        logger.error("⚠️ TELEGRAM_BOT_TOKEN não configurado!")
        exit(1)

    logger.info("🚀 Iniciando o Sentinela VIRGIDREX...")
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    # ... adicionar demais handlers
    app.run_polling()
