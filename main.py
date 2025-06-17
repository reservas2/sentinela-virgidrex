import os
import logging
import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
from dotenv import load_dotenv

# Carrega variáveis do .env
load_dotenv()

# Configuração de logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

# Função para obter variáveis de ambiente com tratamento de erro
def get_env_var(var_name, default_value=None, is_int=False):
    """Função para obter variáveis de ambiente com tratamento de erro"""
    value = os.getenv(var_name, default_value)
    
    # Se o valor ainda contém ${}, significa que não foi substituído
    if value and value.startswith("${") and value.endswith("}"):
        logger.warning(f"Variável {var_name} não foi configurada corretamente. Usando valor padrão.")
        value = default_value
    
    if is_int and value:
        try:
            return int(value)
        except ValueError:
            logger.error(f"Erro ao converter {var_name} para inteiro. Usando valor padrão.")
            return int(default_value) if default_value else 0
    
    return value

# Configuração das variáveis com valores baseados na sua configuração
BOT_TOKEN = get_env_var("TELEGRAM_BOT_TOKEN", "7779664362:AAGXf1YbrDArs6WmedjPGIQqAgPZ8VJ4Tc")
BSCSCAN_API = get_env_var("BSCSCAN_API_KEY", "KXQN4CZXFMCIRPDQKMA9W23TJDSNFB3IE7")
TOKEN_ADDRESS = get_env_var("TOKEN_ADDRESS", "0x653Ac7e8E2Fc011c16bb6aF296BE2A0cc50194FE")
MAX_TOKENS = get_env_var("MAX_TOKENS", "300000000000000000000000", is_int=True)
GRUPO_HOLDERS = get_env_var("GRUPO_HOLDERS", "https://t.me/+VOlYXVwBuTmYaVh")
GRUPO_ESPERA = get_env_var("GRUPO_ESPERA", "https://t.me/+JEQX13GN1Gc3QDYx")

# Converte MAX_TOKENS para o formato correto (300.000 tokens)
MAX_TOKENS_DISPLAY = 300000

# Log das configurações (sem mostrar tokens sensíveis)
logger.info(f"Bot configurado com MAX_TOKENS: {MAX_TOKENS_DISPLAY:,}")
logger.info(f"TOKEN_ADDRESS: {TOKEN_ADDRESS}")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👋 Envie sua carteira BSC (ex: 0x...) ou um print do saldo para ser validado.")

def is_valid_bsc_wallet(wallet: str) -> bool:
    return wallet.startswith("0x") and len(wallet) == 42

def get_token_balance(wallet: str) -> float:
    logger.info(f"Consultando saldo da carteira: {wallet}")
    url = f"https://api.bscscan.com/api?module=account&action=tokenbalance&contractaddress={TOKEN_ADDRESS}&address={wallet}&tag=latest&apikey={BSCSCAN_API}"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        if data["status"] == "1":
            raw_balance = int(data["result"])
            return raw_balance / (10 ** 18)
        else:
            logger.error(f"Erro da API BSCScan: {data.get('message')} - {data.get('result')}")
            return 0
    except requests.exceptions.RequestException as e:
        logger.error(f"Erro ao conectar no BSCScan: {e}")
        return 0

async def handle_wallet(update: Update, context: ContextTypes.DEFAULT_TYPE):
    wallet = update.message.text.strip()
    if not is_valid_bsc_wallet(wallet):
        await update.message.reply_text(
            "🤔❌ O Sentinela não entendeu sua mensagem.\n"
            "Pode ter sido só um erro de digitação... acontece até nos melhores rompimentos.\n"
            "Para continuar, envie sua carteira BSC (ex: 0x...) ou um print do saldo.\n"
            "Print é charme. Blockchain é compromisso."
        )
        return

    balance = get_token_balance(wallet)
    if balance <= MAX_TOKENS_DISPLAY:
        await update.message.reply_text(
            f"✅ O Sentinela deu o sinal verde.\n"
            f"👁️ Sua carteira passou no teste da descentralização: até {MAX_TOKENS_DISPLAY:,} VIRGIDREX, como manda o figurino.\n"
            f"🏛️ Você foi oficialmente admitido no Bloco dos Separados.\n"
            f"👉 Acesse o grupo: {GRUPO_HOLDERS}"
        )
    else:
        await update.message.reply_text(
            f"🧠 Calma, coração. O Sentinela detectou mais de {MAX_TOKENS_DISPLAY:,} VIRGIDREX.\n"
            f"Você será redirecionado para o grupo Corações Apressados.\n"
            f"👉 Entre aqui: {GRUPO_ESPERA}"
        )

async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🖼️ O Sentinela recebeu seu print... mas ele não tem olhos para JPEG.\n"
        "🧠 Para validar sua entrada, cole aqui sua carteira BSC (ex: 0xabc123...)\n"
        "Ou aguarde um admin revisar sua prova visual."
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    help_text = (
        "Olá! Eu sou o bot de validação do $VIRGIDREX.\n"
        "Envie sua carteira BSC ou um print do saldo para começar.\n"
        "Comandos disponíveis:\n"
        "/start - Mensagem de boas-vindas\n"
        "/help - Esta mensagem de ajuda"
    )
    await update.message.reply_text(help_text)

if __name__ == "__main__":
    if not BOT_TOKEN or BOT_TOKEN.startswith("${"):
        logger.error("⚠️ TELEGRAM_BOT_TOKEN não está configurado corretamente!")
        exit(1)
    
    logger.info("🚀 Iniciando o bot Sentinela VIRGIDREX...")
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_wallet))
    app.add_handler(MessageHandler(filters.PHOTO, handle_photo))
    app.run_polling()
