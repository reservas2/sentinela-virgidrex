import anyio
anyio.backend = 'asyncio'

import logging
import os
import asyncio
import requests
from telegram import Update
from telegram.ext import (ApplicationBuilder, CommandHandler, ContextTypes,
                          MessageHandler, filters)
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
BSCSCAN_API_KEY = os.getenv("BSCSCAN_API_KEY")
TOKEN_ADDRESS = os.getenv("TOKEN_ADDRESS")
MAX_TOKENS = int(os.getenv("MAX_TOKENS"))
GRUPO_HOLDERS = os.getenv("GRUPO_HOLDERS")
GRUPO_ESPERA = os.getenv("GRUPO_ESPERA")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👋 Olá! Eu sou o Sentinela VIRGIDREX. Envie sua carteira para verificação.")

def get_token_balance(address):
    url = f"https://api.bscscan.com/api?module=account&action=tokenbalance&contractaddress={TOKEN_ADDRESS}&address={address}&tag=latest&apikey={BSCSCAN_API_KEY}"
    response = requests.get(url)
    data = response.json()
    if data["status"] == "1":
        return int(data["result"])
    return 0

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    address = update.message.text.strip()
    if address.startswith("0x") and len(address) == 42:
        balance = get_token_balance(address)
        if balance >= MAX_TOKENS:
            await update.message.reply_text(f"✅ Você tem {balance:,} VIRGIDREX! Acesso liberado: {GRUPO_HOLDERS}")
        else:
            await update.message.reply_text(f"🚧 Você possui apenas {balance:,} VIRGIDREX. Acesse o grupo de espera: {GRUPO_ESPERA}")
    else:
        await update.message.reply_text("❌ Endereço inválido. Envie um endereço de carteira começando com 0x...")

def main():
    logger.info("🚀 Iniciando o Sentinela VIRGIDREX...")
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    logger.info("✅ Sentinela VIRGIDREX está online e monitorando...")
    app.run_polling()

if __name__ == '__main__':
    main()
