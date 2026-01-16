from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, CallbackQueryHandler

# Ton token Telegram
TOKEN = "8339532089:AAHnTZHjCtzTIqLcdEKXQO3mnz_d2FDBrEs"

# Création du bot
app_bot = ApplicationBuilder().token(TOKEN).build()

# Commande /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    
    texte = """BIENVENUE SUR LE BOT DE PANAME DELIVERY 🗼✨
(Anciennement White Coffee 75)

🔹 Zone : Paris & Île De France 
🔹 Horaires : 14h/02h – 7j/7
🔹 Paiement : Cash uniquement
🔹 Livraison & Meet-up : Rapide et discret

CLIQUEZ SUR LA MINI APP POUR ACCÉDER AUX PRODUITS DISPO, VIDÉOS, MENU, ETC 👇

/start pour démarrer ou redémarrer le bot 🤖"""

    image_url = "https://raw.githubusercontent.com/tmax83270-cpu/telegram-bot-railway/main/panamedelivery.jpg"

    # 🔹 NOUVELLE DISPOSITION DES BOUTONS
    keyboard = [
        [
            InlineKeyboardButton(
                "ℹ️ Information",
                callback_data="info"
            ),
            InlineKeyboardButton(
                "📢 Canal Telegram",
                url="https://t.me/"
            )
        ],
        [
            InlineKeyboardButton(
                "🛒 Ouvrir Mini-App",
                web_app=WebAppInfo(url="https://white-inky.vercel.app/")
            )
        ],
        [
            InlineKeyboardButton(
                "🥔 Canal Potato",
                url="https://ptdym150.org/joinchat/KvW1uaqXsqcevh_qI-BH8Q"
            ),
            InlineKeyboardButton(
                "✉️ Contact",
                callback_data="contact"
            )
        ]
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    await context.bot.send_photo(
        chat_id=chat_id,
        photo=image_url,
        caption=texte,
        reply_markup=reply_markup
    )

# Gestion des boutons
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    data = query.data
    chat_id = query.message.chat_id

    image_info = "https://raw.githubusercontent.com/tmax83270-cpu/telegram-bot-railway/main/info.jpg"
    image_contact = "https://raw.githubusercontent.com/tmax83270-cpu/telegram-bot-railway/main/contact.jpg"

    if data == "info":
        texte_info = """ℹ️ INFORMATIONS ℹ️

Tout est indiqué 👆
On vous livre même si vous êtes dans le fond du 77 ou le fond du 78 ✌️"""
        await context.bot.send_photo(
            chat_id=chat_id,
            photo=image_info,
            caption=texte_info
        )

    elif data == "contact":
        texte_contact = """✉️ CONTACT ✉️

📞 🔵 Telegram : @PanameDelivery

📞 🟢 WhatsApp : +33759873968"""
        await context.bot.send_photo(
            chat_id=chat_id,
            photo=image_contact,
            caption=texte_contact
        )

    await query.answer()

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
app_bot.run_polling()
