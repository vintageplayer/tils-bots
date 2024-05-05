import telebot
from flask import request, jsonify
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
		response_data = {
			'date': 'Published on May 5, 2024',
			'data': """Neuralink's first human patient able to control mouse through thinking, Musk says
Feb 20 (Reuters) - The first human patient implanted with a brain-chip from Neuralink appears to have fully recovered and is able to control a computer mouse using their thoughts, the startup's founder Elon Musk said late on Monday.

"Progress is good, and the patient seems to have made a full recovery, with no ill effects that we are aware of. Patient is able to move a mouse around the screen by just thinking," Musk said in a Spaces event on social media platform X.

https://www.reuters.com/business/healthcare-pharmaceuticals/neuralinks-first-human-patient-able-control-mouse-through-thinking-musk-says-2024-02-20/""",
			'recommendations': ["""Cultural homogenization is an aspect of cultural globalization and refers to the reduction in cultural diversity through the popularization and diffusion of a wide array of cultural symbols—not only physical objects but customs, ideas and values. David E. O'Connor defines it as "the process by which local cultures are transformed or absorbed by a dominant outside culture". Cultural homogenization has been called "perhaps the most widely discussed hallmark of global culture". In theory, homogenization could work in the breakdown of cultural barriers and the global adoption of a single culture.

		    thanks wikipedia. i imagine this can happen in multiple levels, including one starting from our little social friend groups""",
		    """This is another recommendation example.""",
		    """This is yet another recommendation example."""
		    ]
		}
	    return jsonify(response_data)

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