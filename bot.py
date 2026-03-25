import telebot
import os
import threading
from flask import Flask
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

BOT_TOKEN = os.getenv("BOT_TOKEN")

bot = telebot.TeleBot(BOT_TOKEN)

# ===== WEB SERVER FOR RENDER UPTIME =====
app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is Alive"

def run_web():
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)

threading.Thread(target=run_web).start()

# ===== BOT DATA =====
disclaimer = """𝐓𝐇𝐄 𝐒𝐏𝐈𝐑𝐈𝐓 ️:
⚠️ Disclaimer

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

# ===== BUTTON HANDLER =====
@bot.callback_query_handler(func=lambda call: True)
def cb(call):

    if call.data == "learning":
        text = """🧭 Learning Path

This section provides a structured approach
to understanding financial markets step by step.

Phase 1: Basic Understanding
• What markets are
• How price changes occur

Phase 2: Structure Awareness
• Trends and ranges
• Key levels

Phase 3: Risk Thinking
• Exposure awareness
• Capital control

Phase 4: Strategy Concepts
• Entry and exit theory
• Decision frameworks

This path is designed for gradual learning,
not quick results.

Educational reference only.
"""

    elif call.data == "market":
        text = """📊 Market Behavior

Markets move based on supply, demand,
and participant behavior.

This section explains:

• Price movement basics
• Trend formation
• Consolidation phases
• Volatility changes
• Reaction to key levels

Understanding behavior improves clarity,
but does not predict outcomes.

This is conceptual learning only.
"""

    elif call.data == "risk":
        text = """⚖️ Risk Awareness

Every financial activity involves risk.

This section focuses on:

• Understanding exposure
• Managing uncertainty
• Avoiding over-allocation
• Long-term capital thinking
• Emotional control under pressure

Risk cannot be removed,
only managed responsibly.

Educational purposes only.
"""

    elif call.data == "decision":
        text = """🧠 Decision Process

Decision-making plays a key role
in market participation.

This section explores:

• Structured thinking before action
• Avoiding impulsive decisions
• Evaluating conditions logically
• Maintaining consistency
• Learning from past actions

A clear process is more important than speed.

This is educational guidance only.
"""

    elif call.data == "mistake":
        text = """📉 Mistake Analysis

Understanding mistakes is part of learning.

Common areas covered:

• Overtrading behavior
• Emotional reactions
• Lack of structure
• Ignoring risk principles
• Inconsistent decision-making

Improvement comes from awareness,
not repetition.

Educational reference only.
"""
    else:
        return

    bot.answer_callback_query(call.id)
    bot.send_message(call.message.chat.id, text)

# ===== SAFE POLLING LOOP =====
print("Bot Running...")

while True:
    try:
        bot.infinity_polling(timeout=60, long_polling_timeout=60)
    except Exception as e:
        print(e)
