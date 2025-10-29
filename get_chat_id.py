import telebot
from dotenv import load_dotenv
import os

# Load your bot token from .env file
load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")  # make sure .env contains BOT_TOKEN=your_token_here

bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(commands=['start', 'id'])
def send_chat_id(message):
    chat_id = message.chat.id
    chat_title = message.chat.title if message.chat.title else "Private Chat"
    bot.reply_to(message, f"Chat ID: {chat_id}\nChat Name: {chat_title}")

print("Bot is running... Send /id in your group to get the group chat ID.")
bot.infinity_polling()
