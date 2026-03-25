import telebot
import os
import threading
from flask import Flask
from telebot.types import ReplyKeyboardMarkup, KeyboardButton

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

# ===== TEXT DATA =====
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

Inside this bot, you will explore:

• Step-by-step learning paths
• Core market understanding
• Risk and capital awareness
• Strategy thinking (conceptual)
• Self-evaluation guidance

This is not a signal service or advisory platform.
All content is educational and intended
to improve understanding only.

Market conditions vary and outcomes are not guaranteed.

Select a learning path below to begin.
"""

# ===== KEYBOARD =====
def menu():
    kb = ReplyKeyboardMarkup(
        resize_keyboard=True,
        input_field_placeholder="Select Learning Section 👇"
    )
    kb.row(
        KeyboardButton("🧭 Learning Path"),
        KeyboardButton("📊 Market Behavior")
    )
    kb.row(
        KeyboardButton("⚖️ Risk Awareness"),
        KeyboardButton("🧠 Decision Process")
    )
    kb.row(
        KeyboardButton("📉 Mistake Analysis"),
        KeyboardButton("📩 Learning Support")
    )
    return kb

# ===== START =====
@bot.message_handler(commands=['start'])
def start(m):
    sent = bot.send_message(m.chat.id, disclaimer)

    try:
        bot.pin_chat_message(m.chat.id, sent.message_id)
    except:
        pass

    # auto welcome + keyboard open
    bot.send_message(
        m.chat.id,
        welcome,
        reply_markup=menu()
    )

# ===== BUTTON HANDLER =====
@bot.message_handler(func=lambda m: True)
def learning_sections(m):

    if m.text == "🧭 Learning Path":
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

    elif m.text == "📊 Market Behavior":
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

    elif m.text == "⚖️ Risk Awareness":
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

    elif m.text == "🧠 Decision Process":
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

    elif m.text == "📉 Mistake Analysis":
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

    elif m.text == "📩 Learning Support":
        text = """📩 Learning Support

If you have questions about the learning material
or need clarification on specific topics,
you may reach out here:

@jjtrader_00

Support is limited to educational discussion only.
No personal trading advice or signals are provided.
"""
    else:
        return

    bot.send_message(m.chat.id, text)

# ===== SAFE POLLING =====
print("Bot Running...")

while True:
    try:
        bot.infinity_polling(timeout=60, long_polling_timeout=60)
    except Exception as e:
        print(e)
