from flask import Flask
import telebot
from dotenv import load_dotenv
from handlers.routes import configure_routes
from modules import modules
import os
from modules import rag

load_dotenv()

TELEGRAM_TOKEN = os.getenv('NEXT_TELEGRAM_TOKEN')
DBNAME = os.getenv('NEXT_DBNAME')
DB_USER = os.getenv('NEXT_DB_USER')
DB_PASSWORD = os.getenv('NEXT_DB_PASSWORD')
DB_HOST = os.getenv('NEXT_DB_HOST')
DB_PORT = os.getenv('NEXT_DB_PORT')

app = Flask(__name__)
bot = telebot.TeleBot(token=TELEGRAM_TOKEN, threaded=False)
configure_routes(app, bot)
connection = modules.create_connection(DBNAME, DB_USER, DB_PASSWORD, DB_HOST, DB_PORT)

@bot.message_handler(commands=['help'])
def command_help(message):
    bot.reply_to(message,
        ("A tool to help you capture your notes quickly:\n",
         "Later Analyze and link the notes"))

@bot.message_handler(commands=['start'])
def command_start(message):
    record_to_insert = (
        message.message_id,
        message.from_user.id,
        message.from_user.username,
        message.from_user.first_name,
        message.from_user.last_name,
        '',
        message.date
    )
    modules.insert_record(connection, record_to_insert)
    bot.reply_to(message, f"Caputing a new note with ID: {message.message_id}). Please enter your thoughts...")

@bot.message_handler(commands=['end'])
def command_end(message):
    telegram_user_id = message.from_user.id 
    document_record = modules.retrieve_draft_message(connection, telegram_user_id)
    modules.mark_note_as_completed(connection, telegram_user_id)
    if document_record:
        unique_doc_id = str(document_record[0])
        doc_text = document_record[6]
        rag.insert(unique_doc_id, doc_text)
        bot.reply_to(message, f"Notes Stored. You can access them here: {document_record}")

@bot.message_handler(func=lambda message: True, content_types=['text'])
def echo_message(message):
    telegram_user_id = message.from_user.id
    new_doc_text = message.text
    modules.update_doc_text(connection, telegram_user_id, new_doc_text)
