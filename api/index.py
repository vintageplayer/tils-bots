from flask import Flask
import telebot
from dotenv import load_dotenv
from handlers.routes import configure_routes
import os

load_dotenv()

TELEGRAM_TOKEN = os.getenv('NEXT_TELEGRAM_TOKEN')

app = Flask(__name__)
bot = telebot.TeleBot(token=TELEGRAM_TOKEN, threaded=False)
configure_routes(app, bot)

@bot.message_handler(commands=['help'])
def command_start(message):
    bot.reply_to(message,
        ("A tool to help you capture your notes quickly:\n",
         "Later Analyze and link the notes"))

@bot.message_handler(commands=['start'])
def command_start(message):
    bot.reply_to(message, f"Please Enter the Thoughts ({message.message_id}, {message.message_thread_id}, {message.date}, {message.from_user.id}, {message.from_user.first_name}, {message.from_user.last_name}, {message.from_user.username}):\n")

@bot.message_handler(commands=['end'])
def command_start(message):
    bot.reply_to(message, "Notes Stored\n")

@bot.message_handler(func=lambda message: True, content_types=['text'])
def echo_message(message):
    pass
    bot.reply_to(message, f"Please Enter the Thoughts ({message.message_id}, {message.message_thread_id}, {message.text}):\n")
