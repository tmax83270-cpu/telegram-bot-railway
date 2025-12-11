from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, CallbackQueryHandler

# Ton token directement dans le code
TOKEN = "8476960807:AAGLf9Fy05l3A390iBjdigCNOYwtWNnVC0k"

# Crée le bot
app_bot = ApplicationBuilder().token(TOKEN).build()

# Commande /start avec image, texte et boutons
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    texte = "Bienvenue sur mon bot ! 🚀\nChoisis une option :"
    image_url = "https://i.imgur.com/yourimage.jpg"  # remplace par ton image

    # Boutons inline
    keyboard = [
        [InlineKeyboardButton("Option 1", callback_data="option1")],
        [InlineKeyboardButton("Option 2", callback_data="option2")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    # Envoie l'image avec texte et boutons
    await context.bot.send_photo(chat_id=chat_id, photo=image_url, caption=texte, reply_markup=reply_markup)

# Gestion des boutons
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()  # confirme le clic

    if query.data == "option1":
        await query.edit_message_caption(caption="Tu as choisi l’Option 1 ✅")
    elif query.data == "option2":
        await query.edit_message_caption(caption="Tu as choisi l’Option 2 ✅")

# Commandes simples
async def bonjour(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Bonjour ! 😄")

async def aide(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Commandes : /start, /bonjour, /aide")

# Ajout des handlers
app_bot.add_handler(CommandHandler("start", start))
app_bot.add_handler(CommandHandler("bonjour", bonjour))
app_bot.add_handler(CommandHandler("aide", aide))
app_bot.add_handler(CallbackQueryHandler(button_handler))  # gestion des boutons

print("Bot Telegram en ligne...")

# Lancer le bot (long polling)
app_bot.run_polling()
