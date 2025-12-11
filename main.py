from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, CallbackQueryHandler

# Ton token Telegram
TOKEN = "8476960807:AAGLf9Fy05l3A390iBjdigCNOYwtWNnVC0k"

# Crée le bot
app_bot = ApplicationBuilder().token(TOKEN).build()

# Commande /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    
    texte = """🗼💫 PANAME DELIVERY — PLUG PARIS OFFICIEL

🔹 Zone : Paris & Île De France (75,77,78,91,92,93,94,95,60)
🔹 Horaires : 14h/02h – 7j/7
🔹 Paiement : Cash uniquement
🔹 Livraison & Meet-up : Rapide et discret

🔥 Produits disponibles
•Coke ❄️ / • 3mmc 🇳🇱 / • Weed Cali 🇺🇸 / • Weed Hollandaise 🇳🇱 / • 3x Filtré 🍫 / • Jaune Mousseux 🧽

📞 @Panamedelivery 📞"""

    # Image
    image_url = "https://i.ibb.co/fYGqJgSr/IMG-2861.png"

    # Boutons inline
    keyboard = [
        [InlineKeyboardButton("Ouvrir Mini-App", web_app=WebAppInfo(url="https://white-inky.vercel.app/"))],
        [InlineKeyboardButton("Option déco 1", callback_data="none")],
        [InlineKeyboardButton("Option déco 2", callback_data="none")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    # Envoie l'image avec texte et boutons
    await context.bot.send_photo(
        chat_id=chat_id,
        photo=image_url,
        caption=texte,
        reply_markup=reply_markup
    )

# Gestion des boutons décoratifs (ne font rien)
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()  # juste confirme le clic, pas de message

# Commandes simples
async def bonjour(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Bonjour ! 😄")

async def aide(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Commandes : /start, /bonjour, /aide")

# Ajout des handlers
app_bot.add_handler(CommandHandler("start", start))
app_bot.add_handler(CommandHandler("bonjour", bonjour))
app_bot.add_handler(CommandHandler("aide", aide))
app_bot.add_handler(CallbackQueryHandler(button_handler))

print("Bot Telegram en ligne…")

# Lancer le bot (long polling)
app_bot.run_polling()
