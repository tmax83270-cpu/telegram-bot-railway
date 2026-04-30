from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, CallbackQueryHandler
import json
import os

# =========================
# TOKEN BOT
# =========================
TOKEN = "8339532089:AAHnTZHjCtzTIqLcdEKXQO3mnz_d2FDBrEs"

# =========================
# ADMIN ID
# =========================
ADMIN_ID = 123456789  # remplace par ton ID Telegram

# =========================
# USERS STORAGE
# =========================
users_file = "users.json"

if os.path.exists(users_file):
    with open(users_file, "r") as f:
        users = json.load(f)
else:
    users = []


def save_users():
    with open(users_file, "w") as f:
        json.dump(users, f)


# =========================
# BOT INITIALISATION
# =========================
app_bot = ApplicationBuilder().token(TOKEN).build()


# =========================
# /START
# =========================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id

    # 👉 SAVE USER
    if chat_id not in users:
        users.append(chat_id)
        save_users()

    texte = """BIENVENUE SUR LE BOT DE PANAME DELIVERY 🗼✨
(Anciennement White Coffee 75)

🔹 Zone : Paris & Île De France 
🔹 Horaires : 14h/02h – 7j/7
🔹 Paiement : Cash uniquement
🔹 Livraison & Meet-up : Rapide et discret

CLIQUEZ SUR LA MINI APP POUR ACCÉDER AUX PRODUITS DISPO, VIDÉOS, MENU, ETC 👇

/start pour démarrer ou redémarrer le bot 🤖"""

    image_url = "https://raw.githubusercontent.com/tmax83270-cpu/telegram-bot-railway/main/panamedelivery.jpg"

    keyboard = [
        [
            InlineKeyboardButton("🥔 Canal Potato", url="https://ptdym150.org/joinchat/KvW1uaqXsqcevh_qI-BH8Q"),
            InlineKeyboardButton("📢 Canal Telegram", url="https://t.me/+GKfz6FwT-hg5NGJk")
        ],
        [
            InlineKeyboardButton(
                "🛒 Ouvrir Mini-App",
                web_app=WebAppInfo(url="https://white-inky.vercel.app/")
            )
        ],
        [
            InlineKeyboardButton("ℹ️ Information", callback_data="info"),
            InlineKeyboardButton("✉️ Contact", callback_data="contact")
        ]
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    await context.bot.send_photo(
        chat_id=chat_id,
        photo=image_url,
        caption=texte,
        reply_markup=reply_markup
    )


# =========================
# CALLBACK BUTTONS
# =========================
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

📞 Telegram : @PanameDelivery
📞 WhatsApp : +33759873968"""

        await context.bot.send_photo(
            chat_id=chat_id,
            photo=image_contact,
            caption=texte_contact
        )

    await query.answer()


# =========================
# COMMANDES SIMPLE
# =========================
async def bonjour(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Bonjour ! 😄")

async def aide(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Commandes : /start, /bonjour, /aide, /broadcast")


# =========================
# BROADCAST ADMIN
# =========================
async def broadcast(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_chat.id != ADMIN_ID:
        return

    message = " ".join(context.args)

    if not message:
        await update.message.reply_text("❌ Message vide")
        return

    for user in users:
        try:
            await context.bot.send_message(chat_id=user, text=message)
        except:
            pass

    await update.message.reply_text("✅ Message envoyé à tous")


# =========================
# HANDLERS
# =========================
app_bot.add_handler(CommandHandler("start", start))
app_bot.add_handler(CommandHandler("bonjour", bonjour))
app_bot.add_handler(CommandHandler("aide", aide))
app_bot.add_handler(CommandHandler("broadcast", broadcast))
app_bot.add_handler(CallbackQueryHandler(button_handler))


# =========================
# RUN BOT
# =========================
print("Bot Telegram en ligne…")
app_bot.run_polling()
