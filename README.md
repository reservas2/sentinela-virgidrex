# 🛡️ Sentinela VIRGIDREX — Bot de Validação de Carteiras BSC

**Um bot oficial do projeto $VIRGIDREX no Telegram** que valida automaticamente o saldo de tokens em carteiras da Binance Smart Chain (BSC) e direciona os usuários para grupos distintos com base no valor que possuem.

---

## 🚀 Funcionalidades

- Verifica se a carteira BSC fornecida é válida.
- Consulta o saldo de $VIRGIDREX na BSC usando a API do BscScan.
- Direciona usuários com até **300.000 VIRGIDREX** para o **Bloco dos Separados**.
- Direciona usuários com saldo acima disso para o grupo **Corações Apressados**.
- Respostas personalizadas com linguagem temática e tom criativo.
- Reconhece se o usuário enviou um print e orienta o que fazer.

---

## ⚙️ Pré-requisitos

- Python 3.10 ou superior
- Uma conta no Telegram
- Token do bot (criado com o [@BotFather](https://t.me/BotFather))
- Chave da API do [BscScan](https://bscscan.com/myapikey)
- Conta gratuita no [Render](https://render.com/) (ou outro serviço de hospedagem Python)

---

## 🧪 Como Executar Localmente

1. **Clone este repositório:**
   ```bash
   git clone https://github.com/seuusuario/sentinela-virgidrex.git
   cd sentinela-virgidrex
   ```

2. **Instale as dependências:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Crie seu `.env` com as seguintes variáveis:**

   > Você pode usar o `.env.example` como base.

   ```env
   TELEGRAM_BOT_TOKEN="SEU_TOKEN_AQUI"
   BSCSCAN_API_KEY="SUA_CHAVE_AQUI"
   TOKEN_ADDRESS="0x653Ac7e8E2Ec011c168b6eF2968E2A0cc50194FE"
   MAX_TOKENS=300000000000000000000000
   GRUPO_HOLDERS="https://t.me/+VOlyXYwBuThmYmVh"
   GRUPO_ESPERA="https://t.me/+JEQX13GN1Gc3ODYx"
   ```

4. **Execute o bot:**
   ```bash
   python main.py
   ```

---

## 🌐 Hospedagem com Render (grátis)

1. Crie uma conta em [render.com](https://render.com/).
2. Conecte com seu GitHub e selecione este repositório.
3. Configure como serviço web:
   - Runtime: Python
   - Start Command: `python main.py`
   - Adicione as variáveis de ambiente manualmente com os valores do `.env`.

---

## 🧠 Sobre o Projeto $VIRGIDREX

Esse bot é parte do ecossistema da memecoin $VIRGIDREX — um projeto que satiriza o sistema financeiro tradicional com humor, narrativa de separação e foco em descentralização.