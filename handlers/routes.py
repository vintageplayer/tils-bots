import telebot
from flask import request
import time
from dotenv import load_dotenv
import os
from modules import rag

def configure_routes(app, bot):
	bot.remove_webhook()
	time.sleep(0.5)
	WEBHOOK_URL = os.getenv('NEXT_WEBHOOK_URL')
	bot.set_webhook(WEBHOOK_URL)

	@app.route('/')
	def home():
	    return 'Hello, World!'

	@app.route('/posts/<username>')
	def get_user_posts(username):
	    return 'Hello, World!'

	@app.route('/posts/<post_id>')
	def get_post(post_id):
	    return {''}

	@app.route('/about')
	def about():
	    return 'About'

	@app.route('/bot', methods=['POST'])
	def webhook():
		update = telebot.types.Update.de_json(
			request.stream.read().decode('utf-8')
		)
		bot.process_new_updates([update])
		return 'ok', 200