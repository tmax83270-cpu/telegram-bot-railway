from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
    CallbackQueryHandler
)

import json
import os

# =========================
# CONFIG
# =========================

TOKEN = "8690669529:AAHf_mj2dydn7ermmjArgV9JFq49ZlOwKgk"

# TON ID TELEGRAM
ADMIN_ID = 7047054214

USERS_FILE = "users.json"

# =========================
# BOT
# =========================

app_bot = ApplicationBuilder().token(TOKEN).build()

# =========================
# SAUVEGARDE USERS
# =========================

def load_users():
    if not os.path.exists(USERS_FILE):
        return []

    with open(USERS_FILE, "r") as f:
        return json.load(f)

def save_user(user_id):
    users = load_users()

    if user_id not in users:
        users.append(user_id)

        with open(USERS_FILE, "w") as f:
            json.dump(users, f)

# =========================
# START
# =========================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    chat_id = update.effective_chat.id

    # SAUVEGARDE USER
    save_user(chat_id)

    texte = """BIENVENUE SUR LE BOT DE PANAME DELIVERY 🗼✨
(Anciennement White Coffee 75)

🔹 Zone : Paris & Île De France
🔹 Horaires : 14h/02h – 7j/7
🔹 Paiement : Cash uniquement
🔹 Livraison & Meet-up : Rapide et discret

CLIQUEZ SUR LA MINI APP POUR ACCÉDER AUX PRODUITS DISPO 👇
"""

    image_url = "https://raw.githubusercontent.com/tmax83270-cpu/telegram-bot-railway/main/panamedelivery.jpg"

    keyboard = [
        [
            InlineKeyboardButton(
                "🥔 Canal Potato",
                url="https://ptdym150.org/joinchat/KvW1uaqXsqcevh_qI-BH8Q"
            ),
            InlineKeyboardButton(
                "📢 Canal Telegram",
                url="https://t.me/+GKfz6FwT-hg5NGJk"
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
                "ℹ️ Information",
                callback_data="info"
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

# =========================
# BOUTONS
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
"""

        await context.bot.send_photo(
            chat_id=chat_id,
            photo=image_info,
            caption=texte_info
        )

    elif data == "contact":

        texte_contact = """✉️ CONTACT ✉️

📞 Telegram : @PanameDelivery
📞 WhatsApp : +33759873968
"""

        await context.bot.send_photo(
            chat_id=chat_id,
            photo=image_contact,
            caption=texte_contact
        )

    await query.answer()

# =========================
# BROADCAST
# =========================

async def broadcast(update: Update, context: ContextTypes.DEFAULT_TYPE):

    # Vérifie admin
    if update.effective_chat.id != ADMIN_ID:
        return

    # Vérifie message
    if not context.args:
        await update.message.reply_text(
            "Utilisation : /broadcast ton message"
        )
        return

    message = " ".join(context.args)

    users = load_users()

    sent = 0

    for user_id in users:
        try:
            await context.bot.send_message(
                chat_id=user_id,
                text=message
            )
            sent += 1

        except:
            pass

    await update.message.reply_text(
        f"Message envoyé à {sent} utilisateurs."
    )

# =========================
# AUTRES COMMANDES
# =========================

async def bonjour(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Bonjour 😄")

async def aide(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "/start\n/broadcast"
    )

async def users(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if update.effective_chat.id != ADMIN_ID:
        return

    users = load_users()

    texte = "\n".join([str(user) for user in users])

    if texte == "":
        texte = "Aucun utilisateur"

    await update.message.reply_text(texte)

# =========================
# HANDLERS
# =========================

app_bot.add_handler(CommandHandler("start", start))
app_bot.add_handler(CommandHandler("bonjour", bonjour))
app_bot.add_handler(CommandHandler("aide", aide))
app_bot.add_handler(CommandHandler("broadcast", broadcast))
app_bot.add_handler(CallbackQueryHandler(button_handler))
app_bot.add_handler(CommandHandler("users", users))

# =========================
# START BOT
# =========================

print("Bot Telegram en ligne...")
app_bot.run_polling()
