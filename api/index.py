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