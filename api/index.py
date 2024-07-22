from flask import Flask
import telebot
from dotenv import load_dotenv
from handlers.routes import configure_routes
from modules.models import db, Note
import os

load_dotenv()

TELEGRAM_TOKEN = os.getenv('NEXT_TELEGRAM_TOKEN')
DBNAME = os.getenv('NEXT_DBNAME')
DB_USER = os.getenv('NEXT_DB_USER')
DB_PASSWORD = os.getenv('NEXT_DB_PASSWORD')
DB_HOST = os.getenv('NEXT_DB_HOST')
DB_PORT = os.getenv('NEXT_DB_PORT')

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DBNAME}'
db.init_app(app)
bot = telebot.TeleBot(token=TELEGRAM_TOKEN, threaded=False)
configure_routes(app, bot)

@bot.message_handler(commands=['help'])
def command_help(message):
    bot.reply_to(message,
        ("A tool to help you capture your notes quickly:\n",
         "And retain the knowledge overtime using spaced-repition and quizes"))

@bot.message_handler(func=lambda message: True, content_types=['text'])
def echo_message(message):
    print(f'Storing a new note..{message}')
    new_note = Note(
            message_id=message.message_id,
            telegram_user_id=message.from_user.id,
            telegram_username=message.from_user.username,
            telegram_first_name=message.from_user.first_name,
            telegram_last_name=message.from_user.last_name,
            message_text=message.text,
            telegram_creation_date=message.date
        )
    db.session.add(new_note)
    db.session.commit()
    bot.reply_to(message, f"Notes Stored with ID: {message.message_id}).")

if __name__ == '__main__':
    app.run(debug=True, port=5002)

