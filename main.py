# import telebot, os
# from dotenv import load_dotenv

# load_dotenv()
# BOT_TOKEN = os.getenv("BOT_TOKEN")
# print("Loaded token:", BOT_TOKEN)

# bot = telebot.TeleBot(BOT_TOKEN, parse_mode=None)

# @bot.message_handler(func=lambda m: True)
# def echo_all(m):
#     print(f"Message received: {m.text} | chat_id={m.chat.id} | chat_type={m.chat.type}")
#     bot.reply_to(m, "Bot received your message!")

# print("Bot is running...")
# bot.infinity_polling(timeout=60, long_polling_timeout=60)


# import telebot
# from dotenv import load_dotenv
# import os

# # --- Load bot token ---
# load_dotenv()
# BOT_TOKEN = os.getenv("BOT_TOKEN")
# bot = telebot.TeleBot(BOT_TOKEN)

# # --- Global cache for topic names ---
# # Key: message_thread_id, Value: topic name
# TOPIC_CACHE = {}

# # --- Helper function to get topic name ---
# def get_topic_name(message):
#     """
#     Returns the topic name for a message.
#     Checks:
#     1. If the message itself created the topic
#     2. If the message is a reply to the topic creation message
#     3. Fallback to cache
#     """
#     # Check if the message itself created the topic
#     if getattr(message, "forum_topic_created", False):
#         topic_name = message.forum_topic_created.name
#         # Update cache
#         TOPIC_CACHE[message.message_thread_id] = topic_name
#         return topic_name

#     # Check if the message is a reply to the creation message
#     reply = getattr(message, "reply_to_message", None)
#     if reply and getattr(reply, "forum_topic_created", False):
#         topic_name = reply.forum_topic_created.name
#         # Update cache
#         TOPIC_CACHE[message.message_thread_id] = topic_name
#         return topic_name

#     # Fallback to cache
#     return TOPIC_CACHE.get(message.message_thread_id, "Unknown")

# # --- /chat command ---
# @bot.message_handler(commands=['chat'])
# def chat_id(message):
#     chat_id_val = message.chat.id
#     chat_name = message.chat.title if message.chat.title else "Private Chat"
#     bot.reply_to(message, f"Chat ID: {chat_id_val}\nChat Name: {chat_name}")

# # --- /topic command ---
# @bot.message_handler(commands=['topic'])
# def topic_command(message):
#     if getattr(message, "is_topic_message", False):
#         topic_id_val = message.message_thread_id
#         topic_name_val = get_topic_name(message)
#         bot.reply_to(message, f"Topic ID: {topic_id_val}\nTopic Name: {topic_name_val}")
#     else:
#         bot.reply_to(message, "This message is NOT inside a forum topic.")

# # --- Log all forum topic messages ---
# @bot.message_handler(func=lambda m: getattr(m, "is_topic_message", False))
# def handle_topic_message(message):
#     chat_id_val = message.chat.id
#     topic_id_val = message.message_thread_id
#     topic_name_val = get_topic_name(message)

#     # Save to log file
#     with open("telegram_forum_topics.txt", "a", encoding="utf-8") as f:
#         f.write(f"Chat ID: {chat_id_val}, Topic ID: {topic_id_val}, Topic Name: {topic_name_val}\n")

#     print(f"Topic message detected — Chat ID: {chat_id_val}, Topic ID: {topic_id_val}, Topic Name: {topic_name_val}")

# # --- Optional: debug any message ---
# @bot.message_handler(func=lambda m: True)
# def echo_all(m):
#     print(f"Received message: {getattr(m, 'text', '')} in chat {m.chat.id}")

# # --- Start bot ---
# print("Bot is running... Use /chat for chat ID or /topic for topic ID inside forum topics.")
# bot.infinity_polling()


import telebot
from dotenv import load_dotenv
import os

# --- Load bot token ---
load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
bot = telebot.TeleBot(BOT_TOKEN)

# --- Global cache for topic names ---
TOPIC_CACHE = {}  # key: message_thread_id, value: topic name

# --- Helper function to get topic name ---
def get_topic_name(message):
    """
    Returns the topic name for a message.
    Checks:
    1. If the message itself created the topic
    2. If the message is a reply to the topic creation message
    3. Fallback to cache
    """
    if getattr(message, "forum_topic_created", False):
        topic_name = message.forum_topic_created.name
        TOPIC_CACHE[message.message_thread_id] = topic_name
        return topic_name

    reply = getattr(message, "reply_to_message", None)
    if reply and getattr(reply, "forum_topic_created", False):
        topic_name = reply.forum_topic_created.name
        TOPIC_CACHE[message.message_thread_id] = topic_name
        return topic_name

    return TOPIC_CACHE.get(message.message_thread_id, "Unknown")

# --- /chat command ---
@bot.message_handler(commands=['chat'])
def chat_id(message):
    chat_id_val = message.chat.id
    chat_name = message.chat.title if message.chat.title else "Private Chat"
    bot.reply_to(message, f"Chat ID: {chat_id_val}\nChat Name: {chat_name}")
    print(f"💬 /chat command used — Chat ID: {chat_id_val}, Chat Name: {chat_name}")

# --- /topic command ---
@bot.message_handler(commands=['topic'])
def topic_command(message):
    if getattr(message, "is_topic_message", False):
        topic_id_val = message.message_thread_id
        topic_name_val = get_topic_name(message)
        bot.reply_to(message, f"Topic ID: {topic_id_val}\nTopic Name: {topic_name_val}")
        print(f"💬 /topic command used — Topic ID: {topic_id_val}, Topic Name: {topic_name_val}")
    else:
        bot.reply_to(message, "This message is NOT inside a forum topic.")
        print("/topic command used outside a forum topic")

# --- Log all forum topic messages ---
@bot.message_handler(func=lambda m: getattr(m, "is_topic_message", False))
def handle_topic_message(message):
    chat_id_val = message.chat.id
    topic_id_val = message.message_thread_id
    topic_name_val = get_topic_name(message)

    # Save to file
    with open("telegram_forum_topics.txt", "a", encoding="utf-8") as f:
        f.write(f"Chat ID: {chat_id_val}, Topic ID: {topic_id_val}, Topic Name: {topic_name_val}\n")

    # Print to console
    print(f"Topic message detected — Chat ID: {chat_id_val}, Topic ID: {topic_id_val}, Topic Name: {topic_name_val}")

# --- Optional: debug all messages ---
@bot.message_handler(func=lambda m: True)
def echo_all(m):
    text = getattr(m, 'text', None)
    if text:
        print(f"Message received in chat {m.chat.id}: {text}")

# --- Start bot ---
print("Bot is running... Use /chat for chat ID or /topic for topic ID inside forum topics.")
bot.infinity_polling()
