from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# --- Ton token Telegram directement dans le code ---
TOKEN = "8476960807:AAGLf9Fy05l3A390iBjdigCNOYwtWNnVC0k"

# --- Crée le bot Telegram ---
app_bot = ApplicationBuilder().token(TOKEN).build()

# Commande /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Bot actif ! 🚀")
app_bot.add_handler(CommandHandler("start", start))

# Commande /bonjour
async def bonjour(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Bonjour ! 😄")
app_bot.add_handler(CommandHandler("bonjour", bonjour))

# Commande /aide
async def aide(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Commandes : /start, /bonjour, /aide")
app_bot.add_handler(CommandHandler("aide", aide))

print("Bot Telegram en ligne...")

# --- Lancer le bot (long polling) ---
app_bot.run_polling()
