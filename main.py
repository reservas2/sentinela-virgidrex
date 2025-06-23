import os
import logging
import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
from dotenv import load_dotenv

# Carrega variáveis de ambiente
load_dotenv()

# Configuração de logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

# Variáveis de ambiente
BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
BSCSCAN_API = os.getenv("BSCSCAN_API_KEY")
TOKEN_ADDRESS = os.getenv("TOKEN_ADDRESS")

def get_env_var(var_name, default_value=None, is_int=False):
    """Função auxiliar para obter variáveis de ambiente com validação"""
    value = os.getenv(var_name, default_value)
    
    # Se for uma string com ${...}, é inválido
    if value and value.startswith("${") and value.endswith("}"):
        logger.warning(f"⚠️ Variável {var_name} não foi configurada corretamente. Usando valor padrão.")
        value = default_value
    
    if is_int and value:
        try:
            return int(value)
        except ValueError:
            logger.error(f"❌ Erro ao converter {var_name} para inteiro: {value}")
            return int(default_value or 0)
    
    return value

MAX_TOKENS = get_env_var("MAX_TOKENS", "300000000000000000000000", is_int=True)
GRUPO_HOLDERS = os.getenv("GRUPO_HOLDERS")
GRUPO_ESPERA = os.getenv("GRUPO_ESPERA")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Comando /start do bot"""
    await update.message.reply_text(
        "👋 O Sentinela está de prontidão.\n"
        "Envie sua carteira BSC (ex: 0x...) para validação automática.\n\n"
        "Use /help para mais informações."
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Comando /help do bot"""
    help_text = (
        "🛡️ **Sentinela VIRGIDREX - Comandos Disponíveis**\n\n"
        "🔹 `/start` - Inicia o bot\n"
        "🔹 `/help` - Mostra esta mensagem\n\n"
        "**Como usar:**\n"
        "• Envie sua carteira BSC (ex: 0x1234...)\n"
        "• Ou envie um print do seu saldo\n\n"
        "**Validação:**\n"
        "• Até 300.000 VIRGIDREX → Bloco dos Separados\n"
        "• Acima de 300.000 → Corações Apressados\n\n"
        "🧠 Ruptura com humor, código e propósito."
    )
    await update.message.reply_text(help_text, parse_mode='Markdown')

def is_valid_bsc_wallet(wallet):
    """Valida se o endereço da carteira BSC está no formato correto"""
    return wallet.startswith("0x") and len(wallet) == 42

def get_token_balance(wallet):
    """Consulta o saldo de tokens VIRGIDREX na carteira BSC"""
    try:
        logger.info(f"Consultando saldo da carteira: {wallet}")
        
        url = f"https://api.bscscan.com/api?module=account&action=tokenbalance&contractaddress={TOKEN_ADDRESS}&address={wallet}&tag=latest&apikey={BSCSCAN_API}"
        
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        
        data = response.json()
        
        if data["status"] == "1":
            raw_balance = int(data["result"])
            # Converte de wei para tokens (18 casas decimais)
            balance = raw_balance / (10 ** 18)
            logger.info(f"Saldo encontrado: {balance} VIRGIDREX")
            return balance
        else:
            logger.warning(f"Erro na resposta da API: {data}")
            return 0
            
    except requests.exceptions.RequestException as e:
        logger.error(f"Erro de conexão com BSCScan: {e}")
        return None
    except Exception as e:
        logger.error(f"Erro inesperado ao consultar saldo: {e}")
        return None

async def handle_wallet(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Processa carteiras BSC enviadas pelos usuários"""
    wallet = update.message.text.strip()
    
    if not is_valid_bsc_wallet(wallet):
        await update.message.reply_text(
            "🤔❌ O Sentinela não entendeu sua mensagem.\n"
            "Pode ter sido só um erro de digitação... acontece até nos melhores rompimentos.\n\n"
            "Para continuar, envie sua carteira BSC (ex: 0x...) ou um print do saldo.\n"
            "Print é charme. Blockchain é compromisso."
        )
        return

    # Consulta o saldo
    balance = get_token_balance(wallet)
    
    if balance is None:
        await update.message.reply_text(
            "⚠️ O Sentinela teve dificuldades para consultar sua carteira.\n"
            "Tente novamente em alguns instantes ou verifique se o endereço está correto."
        )
        return
    
    if balance <= MAX_TOKENS:
        await update.message.reply_text(
            f"✅ O Sentinela deu o sinal verde.\n"
            f"👁️ Sua carteira passou no teste da descentralização: até 300.000 VIRGIDREX, como manda o figurino.\n\n"
            f"🏛️ Você foi oficialmente admitido no Bloco dos Separados, onde quem rompeu com o sistema agora compartilha memes, teorias e probabilidades de lua.\n\n"
            f"👉 Acesse o grupo: {GRUPO_HOLDERS}\n\n"
            f"Parabéns. Você se separou do sistema — e não precisou de um divórcio judicial."
        )
    else:
        await update.message.reply_text(
            f"🧠 Calma, coração. O Sentinela detectou que você está com mais de 300 mil VIRGIDREX.\n"
            f"Por enquanto, você será redirecionado para o grupo Corações Apressados.\n\n"
            f"Lá a gente troca ideia, segura a ansiedade e espera a próxima fase.\n"
            f"👉 Entre aqui: {GRUPO_ESPERA}\n\n"
            f"O futuro pertence a quem sabe esperar. O meme também."
        )

async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Processa fotos/prints enviados pelos usuários"""
    await update.message.reply_text(
        "🖼️ O Sentinela recebeu seu print... mas ele não tem olhos para JPEG.\n"
        "🧠 Para validar sua entrada, cole aqui sua carteira BSC (ex: 0xabc123...)\n"
        "Ou aguarde um admin revisar sua prova visual na Sala dos Separados.\n\n"
        "O sistema pode ter sido centralizado, mas nosso filtro ainda é humano."
    )

async def handle_other_messages(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Processa outras mensagens que não são carteiras nem fotos"""
    await update.message.reply_text(
        "🤔❌ O Sentinela não entendeu sua mensagem.\n"
        "Pode ter sido só um erro de digitação... acontece até nos melhores rompimentos.\n\n"
        "Para continuar, envie sua carteira BSC (ex: 0x...) ou um print do saldo.\n"
        "Print é charme. Blockchain é compromisso."
    )

def main():
    """Função principal do bot"""
    if not BOT_TOKEN:
        logger.error("⚠️ TELEGRAM_BOT_TOKEN não configurado!")
        exit(1)
    
    if not BSCSCAN_API:
        logger.error("⚠️ BSCSCAN_API_KEY não configurado!")
        exit(1)
    
    if not TOKEN_ADDRESS:
        logger.error("⚠️ TOKEN_ADDRESS não configurado!")
        exit(1)

    logger.info("🚀 Iniciando o Sentinela VIRGIDREX...")
    
    # Cria a aplicação do bot
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    
    # Adiciona os handlers
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(MessageHandler(filters.PHOTO, handle_photo))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_wallet))
    
    logger.info("✅ Sentinela VIRGIDREX está online e monitorando...")
    
    # Inicia o bot
    app.run_polling()

if __name__ == "__main__":
    main()
