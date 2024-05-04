import telebot
from flask import request
import time
from dotenv import load_dotenv
import os


def configure_routes(app, bot):
	bot.remove_webhook()
	time.sleep(0.5)
	WEBHOOK_URL = os.getenv('NEXT_WEBHOOK_URL')
	bot.set_webhook(WEBHOOK_URL)

	@app.route('/')
	def home():
	    return 'Hello, World!'

	@app.route('/about')
	def about():
	    return 'About'

	@app.route('/bot', methods=['POST'])
	def bot():
	    return 'Bot'