from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

import json
import os
from datetime import datetime

=========================

CONFIG

=========================

TOKEN = "8864212024:AAG-6cttyivxxIcRTh4g9djZ3upJ6hgdcdY"

ADMIN_ID = 7047054214

USERS_FILE = "users.json"

=========================

BOT

=========================

app_bot = ApplicationBuilder().token(TOKEN).build()

=========================

USERS

=========================

def load_users():

if not os.path.exists(USERS_FILE):
    return []
try:
    with open(USERS_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)
        if isinstance(data, list):
            return data
        return []
except Exception as e:
    print("Erreur load_users:", repr(e))
    return []

def save_users(users):

try:
    with open(USERS_FILE, "w", encoding="utf-8") as f:
        json.dump(
            users,
            f,
            ensure_ascii=False,
            indent=2
        )
except Exception as e:
    print("Erreur save_users:", repr(e))

def save_user(user_id):

users = load_users()
for user in users:
    if user.get("id") == user_id:
        return
users.append({
    "id": user_id,
    "date": datetime.now().strftime("%Y-%m-%d")
})
save_users(users)
print("Nouvel utilisateur:", user_id)

=========================

START

=========================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

chat_id = update.effective_chat.id
save_user(chat_id)
texte = """BIENVENUE SUR TOULON DELIVERY

Zone : Toulon et alentours
Horaires : 14h - 00h
Paiement : Cash uniquement
Livraison et meet-up : Rapide et discret

Clique sur la Mini-App pour accéder au menu, aux informations et aux promotions.”””

keyboard = [
    [
        InlineKeyboardButton(
            "Canal",
            url="https://t.me/+GKfz6FwT-hg5NGJk"
        ),
        InlineKeyboardButton(
            "Contact",
            callback_data="contact"
        )
    ],
    [
        InlineKeyboardButton(
            "Mini-App",
            web_app=WebAppInfo(
                url="https://toulondelivery.vercel.app/"
            )
        )
    ],
    [
        InlineKeyboardButton(
            "Informations",
            callback_data="info"
        )
    ]
]
markup = InlineKeyboardMarkup(keyboard)
image_url = (
    "https://raw.githubusercontent.com/"
    "tmax83270-cpu/"
    "telegram-bot-railway/"
    "main/Panamedelivery.jpg"
)
try:
    await context.bot.send_photo(
        chat_id=chat_id,
        photo=image_url,
        caption=texte,
        reply_markup=markup
    )
except Exception as e:
    print("Erreur image:", repr(e))
    await context.bot.send_message(
        chat_id=chat_id,
        text=texte,
        reply_markup=markup
    )

=========================

ADMIN PANEL

=========================

def get_admin_keyboard():

return InlineKeyboardMarkup([
    [
        InlineKeyboardButton(
            "Stats",
            callback_data="admin_stats"
        ),
        InlineKeyboardButton(
            "Users",
            callback_data="admin_users"
        )
    ],
    [
        InlineKeyboardButton(
            "Broadcast",
            callback_data="admin_broadcast"
        ),
        InlineKeyboardButton(
            "Refresh",
            callback_data="admin_refresh"
        )
    ]
])

async def admin_panel(update: Update, context: ContextTypes.DEFAULT_TYPE):

if update.effective_chat.id != ADMIN_ID:
    return
await update.effective_message.reply_text(
    "ADMIN DASHBOARD",
    reply_markup=get_admin_keyboard()
)

=========================

STATS

=========================

async def send_stats(query):

users = load_users()
text = "STATS\n\n"
text += f"Total utilisateurs : {len(users)}"
await query.message.reply_text(text)

=========================

USERS

=========================

async def send_users(query):

users = load_users()
if not users:
    await query.message.reply_text(
        "Aucun utilisateur."
    )
    return
text = "USERS\n\n"
for user in users:
    line = f"ID : {user.get('id')}\n"
    if len(text + line) > 3500:
        await query.message.reply_text(text)
        text = "USERS SUITE\n\n"
    text += line
await query.message.reply_text(text)

=========================

CALLBACKS

=========================

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):

query = update.callback_query
if not query:
    return
await query.answer()
data = query.data
# =========================
# INFO
# =========================
if data == "info":
    texte = """INFORMATIONS

Zone : Toulon et alentours

Horaires : 14h - 00h

Paiement :
Cash uniquement

Livraison et meet-up rapide et discret”””

    await query.message.reply_text(texte)
# =========================
# CONTACT
# =========================
elif data == "contact":
    texte = """CONTACT

Telegram : @ToulonDelivery

WhatsApp : TON_NUMERO”””

    await query.message.reply_text(texte)
# =========================
# ADMIN
# =========================
elif data.startswith("admin_"):
    if query.message.chat_id != ADMIN_ID:
        await query.answer(
            "Acces refuse",
            show_alert=True
        )
        return
    if data == "admin_stats":
        await send_stats(query)
    elif data == "admin_users":
        await send_users(query)
    elif data == "admin_broadcast":
        await query.message.reply_text(
            "Utilise :\n\n"
            "/broadcast Ton message"
        )
    elif data == "admin_refresh":
        await query.message.edit_text(
            "ADMIN DASHBOARD",
            reply_markup=get_admin_keyboard()
        )

=========================

BROADCAST

=========================

async def broadcast(update: Update, context: ContextTypes.DEFAULT_TYPE):

if update.effective_chat.id != ADMIN_ID:
    return
if not context.args:
    await update.message.reply_text(
        "Utilisation :\n"
        "/broadcast ton message"
    )
    return
message = " ".join(context.args)
users = load_users()
sent = 0
failed = 0
for user in users:
    user_id = user.get("id")
    try:
        await context.bot.send_message(
            chat_id=user_id,
            text=message
        )
        sent += 1
    except Exception as e:
        print(
            "Erreur broadcast:",
            user_id,
            repr(e)
        )
        failed += 1
await update.message.reply_text(
    f"Broadcast termine\n\n"
    f"Envoyes : {sent}\n"
    f"Erreurs : {failed}"
)

=========================

ERROR HANDLER

=========================

async def error_handler(update, context):

print("ERREUR BOT:", repr(context.error))

=========================

HANDLERS

=========================

app_bot.add_handler(
CommandHandler(“start”, start)
)

app_bot.add_handler(
CommandHandler(“admin”, admin_panel)
)

app_bot.add_handler(
CommandHandler(“broadcast”, broadcast)
)

app_bot.add_handler(
CallbackQueryHandler(button_handler)
)

app_bot.add_error_handler(
error_handler
)

=========================

START BOT

=========================

print(“Bot en ligne”)

app_bot.run_polling()
