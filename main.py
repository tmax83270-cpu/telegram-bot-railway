from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

import json
import os

# =========================
# CONFIG
# =========================

TOKEN = "8690669529:AAHf_mj2dydn7ermmjArgV9JFq49ZlOwKgk"
ADMIN_ID = 7047054214

USERS_FILE = "users.json"

# =========================
# BOT INIT
# =========================

app_bot = ApplicationBuilder().token(TOKEN).build()

# =========================
# USERS SYSTEM
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

    # save user
    save_user(chat_id)

    texte = """BIENVENUE SUR PANAME DELIVERY 🗼

Accède à la mini app ci-dessous 👇"""

    keyboard = [
        [
            InlineKeyboardButton(
                "🛒 Ouvrir Mini-App",
                web_app=WebAppInfo(url="https://white-inky.vercel.app/")
            )
        ]
    ]

    await context.bot.send_message(
        chat_id=chat_id,
        text=texte,
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

# =========================
# BROADCAST (ADMIN ONLY)
# =========================

async def broadcast(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if update.effective_chat.id != ADMIN_ID:
        return

    if not context.args:
        await update.message.reply_text("Utilisation : /broadcast message")
        return

    message = " ".join(context.args)

    users = load_users()

    sent = 0

    for user_id in users:
        try:
            await context.bot.send_message(chat_id=user_id, text=message)
            sent += 1
        except:
            pass

    await update.message.reply_text(f"Envoyé à {sent} utilisateurs")

# =========================
# USERS LIST (ADMIN ONLY)
# =========================

async def users_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if update.effective_chat.id != ADMIN_ID:
        return

    users = load_users()

    if not users:
        await update.message.reply_text("Aucun utilisateur")
        return

    text = "LISTE DES USERS :\n\n"

    for u in users:
        text += f"{u}\n"

    await update.message.reply_text(text)

# =========================
# HANDLERS
# =========================

app_bot.add_handler(CommandHandler("start", start))
app_bot.add_handler(CommandHandler("broadcast", broadcast))
app_bot.add_handler(CommandHandler("users", users_cmd))

# =========================
# START BOT
# =========================

print("Bot en ligne...")
app_bot.run_polling()
