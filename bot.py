import telebot
import os
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

BOT_TOKEN = os.getenv("BOT_TOKEN")

bot = telebot.TeleBot(BOT_TOKEN)

disclaimer = """⚠️ Disclaimer

This bot is created for educational purposes only.
Trading involves financial risk and may result in loss.
We do not provide financial advice, signals, or guaranteed results.

By continuing, you confirm that you understand and accept this.
"""

welcome = """Welcome to the JJ Learning Hub 📘

This assistant is designed to guide individuals
through structured learning related to financial markets,
risk awareness, and decision-making concepts.

Select a learning path below to begin.
"""

def menu():
    kb = InlineKeyboardMarkup(row_width=2)
    kb.add(
        InlineKeyboardButton("🧭 Learning Path", callback_data="learning"),
        InlineKeyboardButton("📊 Market Behavior", callback_data="market"),
        InlineKeyboardButton("⚖️ Risk Awareness", callback_data="risk"),
        InlineKeyboardButton("🧠 Decision Process", callback_data="decision"),
        InlineKeyboardButton("📉 Mistake Analysis", callback_data="mistake"),
        InlineKeyboardButton("📩 Learning Support", url="https://t.me/jjtrader_00")
    )
    return kb

@bot.message_handler(commands=['start'])
def start(m):
    sent = bot.send_message(m.chat.id, disclaimer)

    try:
        bot.pin_chat_message(m.chat.id, sent.message_id)
    except:
        pass

    bot.send_message(m.chat.id, welcome, reply_markup=menu())

@bot.callback_query_handler(func=lambda call: True)
def cb(call):

    data = {
        "learning": "🧭 Learning Path section opened",
        "market": "📊 Market Behavior section opened",
        "risk": "⚖️ Risk Awareness section opened",
        "decision": "🧠 Decision Process section opened",
        "mistake": "📉 Mistake Analysis section opened",
    }

    if call.data in data:
        bot.send_message(call.message.chat.id, data[call.data])

bot.infinity_polling()
