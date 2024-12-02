import os
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, CallbackContext
from database import BotDatabase

# Настраиваем логирование
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

# Получаем токен бота из переменной окружения
TOKEN = os.getenv("BOT_TOKEN")
db = BotDatabase()

async def start(update: Update, context: CallbackContext):
    """Команда /start"""
    await update.message.reply_text("Привет! Используйте /in, чтобы добавиться в список.")

async def in_command(update: Update, context: CallbackContext):
    """Добавить пользователя в список"""
    user = update.effective_user
    chat_id = update.effective_chat.id

    db.add_user(user.id, user.username or user.first_name)
    db.add_user_to_chat(chat_id, user.id)

    await update.message.reply_text(f"{user.first_name}, вы добавлены в список!")

async def out_command(update: Update, context: CallbackContext):
    """Удалить пользователя из списка"""
    user = update.effective_user
    chat_id = update.effective_chat.id

    db.delete_user_from_chat(chat_id, user.id)

    await update.message.reply_text(f"{user.first_name}, вы удалены из списка!")

async def all_command(update: Update, context: CallbackContext):
    """Упомянуть всех участников чата"""
    chat_id = update.effective_chat.id
    users = db.get_users_from_chat(chat_id)

    if
