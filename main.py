from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import os

# Ton token Telegram
TOKEN = "8476960807:AAGLf9Fy05l3A390iBjdigCNOYwtWNnVC0k"

# Crée le bot
app_bot = ApplicationBuilder().token(TOKEN).build()

# Commande /start avec image, texte et boutons
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    
    # Texte à afficher
    texte = "Bienvenue sur mon bot ! 🚀\nChoisis une option :"
    
    # Image à envoyer (URL ou fichier local)
    image_url = "https://example.com/ton_image.jpg"  # remplace par ton image
    
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
    await query.answer()
    
    if query.data == "option1":
        await query.edit_message_caption(caption="Tu as choisi l’Option 1 ✅")
    elif query.data == "option2":
        await query.edit_message_caption(caption="Tu as choisi l’Option 2 ✅")

# Ajout des handlers
app_bot.add_handler(CommandHandler("start", start))
app_bot.add_handler(CommandHandler("bonjour", lambda u, c: c.bot.send_message(u.effective_chat.id, "Bonjour ! 😄")))
app_bot.add_handler(CommandHandler("aide", lambda u, c: c.bot.send_message(u.effective_chat.id, "Commandes : /start, /bonjour, /aide")))

# Callback pour les boutons inline
from telegram.ext import CallbackQueryHandler
app_bot.add_handler(CallbackQueryHandler(button_handler))

print("Bot Telegram en ligne...")

# Lance le bot
app_bot.run_polling()
