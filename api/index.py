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

@bot.message_handler(commands=['start', 'help'])
def command_start(message):
    bot.reply_to(message, 
        ("Hi there, I am EchoBot.\n"
        "I am here to echo your kind words back to you"))

@bot.message_handler(func=lambda message: True, content_types=['text'])
def echo_message(message):
    bot.reply_to(message, message.text)
