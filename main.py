import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import threading
import os
from flask import Flask

# Paste your bot tokens here in this format
TOKENS = [
    "8668483286:AAHbbNqjWZM7pXQ4MB6auE07EkVobrx6X44",
    "8716277413:AAGbu2U6eI4aR1vIYNKBncNlIZSMtbQUzJo"
]

def create_and_run_bot(token):
    """Function to initialize and run a single bot."""
    bot = telebot.TeleBot(token)

    @bot.message_handler(commands=['start'])
    def send_welcome(message):
        markup = InlineKeyboardMarkup()
        # Adding the button that links to YouTube
        open_button = InlineKeyboardButton("🌟 Open YouTube 🌟", url="https://youtube.com")
        markup.add(open_button)

        # Engaging message using Markdown
        welcome_text = (
            "🚀 **Welcome to the Hub!** 🚀\n\n"
            "Here is how to get started:\n\n"
            "👉 **Step 1:** Click the open button below.\n"
            "👉 **Step 2:** Explore the video library.\n"
            "👉 **Step 3:** Enjoy the content!\n\n"
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
    # We use none_stop=True to keep it running smoothly in the thread
    bot.polling(none_stop=True)

# Loop through the tokens and start a background thread for each bot
for token in TOKENS:
    # We use daemon=True so the threads close automatically when the web server closes
    thread = threading.Thread(target=create_and_run_bot, args=(token,), daemon=True)
    thread.start()

# --- Render Web Service Requirement ---
# This dummy Flask app gives Render the web server it expects on port 10000
app = Flask(__name__)

@app.route('/')
def health_check():
    return "All Telegram bots are running successfully!"

if __name__ == "__main__":
    # Render assigns a specific port dynamically, we must bind to it
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
