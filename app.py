import os
import logging
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from telegram.utils.helpers import mention_markdown
from database import BotDatabase

logging.basicConfig(
    filename='logs.log',
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# SQLite-файл для базы данных
db = BotDatabase('database.db')

TOKEN = os.getenv('TOKEN')

def start_command(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Добро пожаловать! Введите /in, чтобы присоединиться.")

def in_command(update, context):
    chat_id = update.effective_chat.id
    user = update.effective_user
    user_name = user.username or user.first_name or "anonymous"
    db.add_user(user.id, user_name)
    db.add_user_to_chat(chat_id, user.id)
    context.bot.send_message(chat_id=chat_id, text=f"Вы добавлены, {user_name}!")

def out_command(update, context):
    chat_id = update.effective_chat.id
    user = update.effective_user
    user_name = user.username or user.first_name or "anonymous"
    db.delete_user_from_chat(chat_id, user.id)
    context.bot.send_message(chat_id=chat_id, text=f"Вы удалены, {user_name}.")

def all_command(update, context):
    chat_id = update.effective_chat.id
    user_list = db.get_users_from_chat(chat_id)
    if not user_list:
        context.bot.send_message(chat_id=chat_id, text="Пользователей нет. Введите /in для добавления.")
    else:
        mentions = [mention_markdown(user_id, username, version=2) for user_id, username in user_list]
        context.bot.send_message(chat_id=chat_id, text=" ".join(mentions), parse_mode="MarkdownV2")

def stats_command(update, context):
    users_count = db.count_users()[0]
    chats_count = db.count_chats()[0]
    context.bot.send_message(chat_id=update.effective_chat.id, text=f"Всего пользователей: {users_count}\nЧатов: {chats_count}")

def unknown_command(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Неизвестная команда.")

updater = Updater(token=TOKEN, use_context=True)
dispatcher = updater.dispatcher

dispatcher.add_handler(CommandHandler('start', start_command))
dispatcher.add_handler(CommandHandler('in', in_command))
dispatcher.add_handler(CommandHandler('out', out_command))
dispatcher.add_handler(CommandHandler('all', all_command))
dispatcher.add_handler(CommandHandler('stats', stats_command))
dispatcher.add_handler(MessageHandler(Filters.command, unknown_command))

updater.start_polling()
updater.idle()

db.close()
