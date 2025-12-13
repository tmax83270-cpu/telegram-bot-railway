from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, CallbackQueryHandler

# Ton token Telegram
TOKEN = "8476960807:AAGLf9Fy05l3A390iBjdigCNOYwtWNnVC0k"

# Création du bot
app_bot = ApplicationBuilder().token(TOKEN).build()

# Commande /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    
    texte = """BIENVENUE SUR LE BOT DE PANAME DELIVERY 🗼✨
(Anciennement White Coffee 75)

🔹 Zone : Paris & Île De France (75,77,78,91,92,93,94,95,60)
🔹 Horaires : 14h/02h – 7j/7
🔹 Paiement : Cash uniquement
🔹 Livraison & Meet-up : Rapide et discret

👉 CLIQUEZ SUR LA MINI APP POUR ACCÉDER AUX PRODUITS DISPO, VIDÉOS, MENU, ETC 👇

📞 @PanameDelivery 📞"""

    # Image Imgur
    image_url = "https://i.imgur.com/C8lV0GT.jpeg"

    # Boutons inline
    keyboard = [
        [InlineKeyboardButton("🛒 Ouvrir Mini-App", web_app=WebAppInfo(url="https://white-inky.vercel.app/"))],
        [InlineKeyboardButton("📢 Canal Telegram", url="https://t.me/+2WYuiyhQblMzMGQ0")],
        [InlineKeyboardButton("🥔 Canal Potato", url="https://ptdym150.org/joinchat/KvW1uaqXsqcevh_qI-BH8Q")],
        [InlineKeyboardButton("🔄 Canal Retour Client", url="https://ptdym150.org/joinchat/Z72cV4vSa_ubtLHk3WYgFg")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    # Envoie l'image avec texte et boutons
    await context.bot.send_photo(
        chat_id=chat_id,
        photo=image_url,
        caption=texte,
        reply_markup=reply_markup
    )

# Gestion des boutons (callback_data si besoin)
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()  # confirme le clic

# Autres commandes
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
