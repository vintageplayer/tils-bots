from flask import Flask
import telebot
from dotenv import load_dotenv
import os

load_dotenv()

TELEGRAM_TOKEN = os.getenv('NEXT_TELEGRAM_TOKEN')

app = Flask(__name__)
bot = telebot.TeleBot(token=TELEGRAM_TOKEN, threaded=False)

@app.route('/')
def home():
    return 'Hello, World!'

@app.route('/about')
def about():
    return 'About'

@app.route('/bot')
def bot():
    return 'Bot'
